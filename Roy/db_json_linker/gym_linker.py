
from Roy.python_objects.python_objects import GymClassTemplate

class GymLinker():
    def __init__(self, gym_classes_template_list, json_gym_classes_template ):
        self.gym_classes_template_list = gym_classes_template_list
        self.json_gym_classes_template = json_gym_classes_template

    @classmethod
    def from_db_json(cls, courses_templates):
        gym_classes_list = []
        for gym_name, description in courses_templates.items():
            gym_classes_list.append(GymClassTemplate(gym_name, description))
        return cls(gym_classes_list, courses_templates)

    @classmethod
    def from_python_obj(cls, classes_template_list):
        json_gym_classes_template = {}
        for class_template in classes_template_list:
            json_gym_classes_template[class_template.name] = class_template.description
        return cls(classes_template_list, json_gym_classes_template)