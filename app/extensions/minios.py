from minio import Minio
from app.settings import settings


class MinioClient(object):
    """存储桶"""

    def __init__(self) -> None:
        self.bucket_name = settings.PROJECT_NAME
        self.minio_client = Minio(
            settings.MINIO_HOST,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        if not self.exists_bucket():
            self.minio_client.make_bucket(self.bucket_name)

    def exists_bucket(self):
        return self.minio_client.bucket_exists(self.bucket_name)

    def fget_object(self, object_name, file_path):
        """下载文件保存在本地"""
        self.minio_client.fget_object(self.bucket_name, object_name, file_path)

    def fput_object(self, file, file_path):
        self.minio_client.fput_object(self.bucket_name, file, file_path)

    def put_object(self, object_name, file_data, file_size):
        """流式上传文件"""
        self.minio_client.put_object(self.bucket_name, object_name, file_data, file_size)

    @property
    def client(self) -> Minio:
        """客户端"""
        return self.minio_client

    def stat_object(self, file):
        """获取文件对象数据"""
        return self.client.stat_object(self.bucket_name, file)

if __name__ == '__main__':
    print("1")
