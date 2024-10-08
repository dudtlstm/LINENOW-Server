from django.db import models
from django.utils import timezone
# Create your models here.
def image_upload_path(instance, filename):
    event_id = instance.booth.event.id
    booth_id = instance.booth.id
    return f'event_{event_id}/booth_{booth_id}/{filename}'

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="행사명")
    
    def __str__(self):
        return self.name
    
class Booth(models.Model):
    OPERATED_STATUS = [
        ('not_started', 'Not Started'), # DB에 저장되는 값, 사용자에게 보여지는 값 순
        ('operating', 'Operating'),
        ('finished', 'Finished'),
        ('paused', 'Paused')
    ]

    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="booths") 
    name = models.CharField(max_length=100, verbose_name="부스명")
    description = models.TextField(verbose_name="부스 설명")
    caution = models.TextField(verbose_name="부스 유의사항")
    location = models.CharField(max_length=255, verbose_name="부스 위치")
    is_operated = models.CharField(max_length=100, choices=OPERATED_STATUS, verbose_name="운영 여부")
    open_time = models.DateTimeField(verbose_name="시작 시간")
    close_time = models.DateTimeField(verbose_name="마감 시간")

    def save(self, *args, **kwargs):
        if self.is_operated == 'operating' and self.open_time is None:
            self.open_time = timezone.now()
        elif self.is_operated == 'finished' and self.close_time is None:
            self.close_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class BoothMenu(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=100, verbose_name="메뉴 이름")
    price = models.IntegerField(verbose_name="가격")

    def __str__(self):
        return f'{self.name} - {int(self.price):,}원'
    
class BoothImage(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name="boothimages")
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    
    def __str__(self):
        return f'{self.booth.name} - {self.id}'