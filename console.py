#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
       This class defines the attributes and methods for the
       AirBnB clone console
    """
    __file_path = "file.json"
    prompt = '(hbnb) '
    cls_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
            }

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        print()  # Print a newline before exiting
        return True

    def do_help(self, arg):
        """
           List available commands with 'help' or detailed
           help with 'help <command>'
        """
        cmd.Cmd.do_help(self, arg)

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "create": self.do_create,
            "update": self.do_update,
            "count": self.do_count
        }
        # Match all characters before a period
        pattern = r'^.*?(?=\.)'
        match = re.search(pattern, line)
        if match:
            match_class = match.group()
            if match_class not in HBNBCommand.cls_dict.keys():
                print("** class doesn't exist **")
                return
        else:
            print("** unknown syntax **")

        # Match characters after a period and before an opening parenthesis
        pattern_2 = r'\.(.*?)\('
        match_2 = re.search(pattern_2, line)
        if match_2:
            match_cmd = match_2.group(1)
            for key, value in argdict.items():
                if match_cmd not in argdict.keys():
                    print("** unknown syntax **")
                    return
                lst = list(argdict.keys())
                pattern_3 = r'\((.*?)\)'
                match_3 = re.search(pattern_3, line)
                pattern_4 = r'"(.*?)"'
                match_4 = re.search(pattern_4, line)
                pattern_5 = r"'(.*?)'"
                match_5 = re.search(pattern_5, line)
                if key == lst[0] or key == lst[3] or key == lst[5]:
                    if match_cmd == key:
                        value(match_class)
                        return
                elif key == lst[4]:
                    if match_cmd == key:
                        if match_3:
                            match_txt = match_3.group(1)
                            lst_args = re.split(r',', match_txt)
                            list_args = []
                            for lst_arg in lst_args:
                                lst_arg = lst_arg.strip()
                                lst_arg = lst_arg.strip("'")
                                lst_arg = lst_arg.strip('"')
                                list_args.append(lst_arg)
                            if match_txt == '':
                                value(match_class)
#                                print("** instance id missing **")
                                return
                            if len(list_args) == 1:
                                value("{} {}".format(
                                    match_class, list_args[0]))
#                                print("** attribute name missing **")
                                return
                            pattern_6 = r'\{([^}]+)\}'
                            match_6 = re.search(pattern_6, match_txt)
                            if match_6:
                                pattern_7 = r'(?<=,).*'
                                match_7 = re.search(pattern_7, match_txt)
                                match_dict = match_7.group().strip()
                                match_dict = match_dict.strip("{}")
                                kwargs_pairs = match_dict.split(',')
                                final_dict = {}
                                for pair in kwargs_pairs:
                                    pair = pair.strip()
                                    key_a, val_a = pair.split(':')
                                    key_a, val_a = key_a.strip(), val_a.strip()
                                    key_a, val_a = key_a.strip("'"),\
                                        val_a.strip("'")
                                    key_a, val_a = key_a.strip('"'),\
                                        val_a.strip('"')
                                    final_dict[key_a] = val_a
                                for key_0, val_0 in final_dict.items():
                                    value("{} {} {} {}".format(match_class,
                                          list_args[0], key_0, val_0))
                            else:
                                if len(list_args) == 2:
                                    value("{} {} {}".format(match_class,
                                          list_args[0], list_args[1]))
                                    return
                                elif len(list_args) == 3:
                                    argm_string = "{} {} {} {}".format(match_class,
                                          list_args[0], list_args[1], list_args[2])
                                    value(argm_string)
                        else:
                            print("** unknown syntax **")
                            return
                else:
                    if match_3 or match_4 or match_5:
                        if match_3 and match_4:
                            match_text = match_4.group(1)
                        elif match_3 and match_5:
                            match_text = match_5.group(1)
                        elif match_3:
                            match_text = match_3.group(1)
                        if match_cmd == key:
                            value("{} {}".format(match_class, match_text))
                            return
                    else:
                        value(match_class)
                        return

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print its id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        for key in HBNBCommand.cls_dict.keys():
            if class_name == key:
                new_instance = eval(key)()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
           Print the string representation of an instance
           based on class name and id
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """
           Delete an instance based on class name and id, and save the change
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()
        print("Instance {:s} deleted".format(instance_id))

    def do_all(self, arg):
        """
           Print all string representations of instances
           based on class name (or all)
        """
        storage.reload()
        class_name = arg
        all_objects = storage.all()
        if class_name:
            if class_name not in HBNBCommand.cls_dict.keys():
                print("** class doesn't exist **")
                return
            for key, object in all_objects.items():
                if key.startswith(class_name):
                    objects = [str(object)]
                    print(objects)
        else:
            for object in all_objects.values():
                objects = [str(object)]
                print(objects)

    def do_update(self, arg):
        """
           Update an instance's attribute based
           on class name, id, and attribute name
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objects = storage.all()
        if key not in all_objects.keys():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value = args[3]
        instance = all_objects[key]
        setattr(instance, attribute_name, attribute_value)
        instance.save()
        print("Record Updated")

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        with open(HBNBCommand.__file_path, "r") as file:
            loaded_objects = json.load(file)
            counter = 0
            for key, value in loaded_objects.items():
                if value["__class__"] == class_name:
                    counter += 1
            print(counter)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
