# --ignore=errors      skip errors and warnings (e.g. E4,W) (default:E121,E123,E126,E226,E24,E704,W503)     # pylint: disable=line-too-long
from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = [
        CarMake.objects.create(
            name=data["name"], description=data["description"]
        )
        for data in car_make_data
    ]

    # pylint: disable=line-too-long
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},  # pylint: disable=line-too-long
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},  # pylint: disable=line-too-long
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},  # pylint: disable=line-too-long
        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},  # pylint: disable=line-too-long
        {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},  # pylint: disable=line-too-long
        {"name": "E-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},  # pylint: disable=line-too-long
        {"name": "A4", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": car_make_instances[4]},
    ]
    # pylint: enable=line-too-long

    for data in car_model_data:
        CarModel.objects.create(
            name=data["name"],
            car_make=data["car_make"],
            type=data["type"],
            year=data["year"],
        )
