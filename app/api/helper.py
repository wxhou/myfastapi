import re
import json
import httpx
import traceback
from user_agents import parse
from fastapi import Depends, Request
from app.extensions import get_redis, AsyncRedis
from app.utils.logger import logger




async def get_ipv4_address(ipv4, _redis):
    """_summary_
    获取IP对应所在地及运营商
        太平洋免费API: http://whois.pconline.com.cn/ipJson.jsp
        返回信息:
        {
            "ip":"218.192.3.42", "pro":"广东省", "city":"广州市",
            "proCode":"440000", "cityCode":"440100", "region":"", "regionCode":"0",
            "addr":"广东省广州市 广州大学纺织服装学院",
            "regionNames":"","err":""
        }
    Args:
        ip_addr (_type_): _description_

    Returns:
        _type_: _description_
    """
    key = "get_ipv4_address_%s" % ipv4
    result = await _redis.get(key)
    if result:
        return result.decode()

    try:
        if not re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ipv4):
            return None
        URL = "http://whois.pconline.com.cn/ipJson.jsp?ip=%s&json=true" % ipv4
        async with httpx.AsyncClient() as client:
            req = await client.get(URL)
            logger.debug(req.text)
            addr = json.loads(req.text.replace('\n',''))['addr']
            if addr:
                await _redis.set(key, addr, ex=60*60*8)
            return addr
    except Exception:
        logger.critical(traceback.format_exc())
        return None



async def get_client_info(
    request: Request,
    redis: AsyncRedis = Depends(get_redis),
):
    """获取客户端的信息
    """

    async def get_request_ip():
        if 'X-Real-Ip' in request.headers:
            ipaddr = request.headers['X-Real-Ip']
        elif request.headers.getlist('X-Forworded-For'):
            ipaddr = request.headers.getlist('X-Forworded-For')[0]
        else:
            ipaddr = request.client.host
        return ipaddr


    user_agent = parse(request.headers.get("User-Agent"))

    _ip_addr = await get_request_ip()
    result = {
        'ip_addr': _ip_addr,
        'ip_position': await get_ipv4_address(_ip_addr, redis),
        'client_brower': user_agent.browser.family + user_agent.browser.version_string,
        'client_type': user_agent.os.family + user_agent.os.version_string
    }
    return result




