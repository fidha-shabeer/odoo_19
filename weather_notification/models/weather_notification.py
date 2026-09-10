# -*- coding: utf-8 -*-
from odoo import models, api,fields
import requests


class WeatherNotification(models.Model):
    _name = "weather.notification"

    @api.model
    def get_weather(self):
        print("weather")
        API_KEY = "5be6c2fe9646823a6e7b4ff463529e8e"


        user = self.env.user
        lon = user.longitude
        print("longitute", lon)
        lat = user.latitude
        print("latitude", lat)
        location = user.location
        print("location", location)
        type = user.type
        print("type", type)


        if type == "coordinates":
            print("yes coordinates")
            url =f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url)
            data = response.json()
        else:
            print("location selected")
            url=f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
            response = requests.get(url)
            data = response.json()
        print(data)
        time = fields.Datetime.now()
        return {
            'time':time ,
            'data': data,
            'weather': data['weather'][0]['description'],
            'temp': data['main']['temp'],
        }


