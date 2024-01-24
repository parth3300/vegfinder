from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    CATEGORY_CHOICES = [('restaurant', 'restaurant'),
                        ('dharmshala', 'dharmshala')]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    images = models.ImageField(upload_to='vegfinder/images')
    block_no = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='restaurants_in_city')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='restaurants_in_state')
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='restaurants_in_country')
    pincode = models.IntegerField()
    contact = models.BigIntegerField()
    ratings = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    ratings = models.CharField(max_length=1, choices=RATING_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.ratings
