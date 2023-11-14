import argh, yaml, os, shutil

TEMPLATE_PATH = os.path.join("templates")
FILES_PATH = os.path.join("files")

def read_data_from_input(input_path: str) -> list:
    # Read configurations for validation-nodes from input_path. Note that input_path should lead to *.yml-file
    with open(input_path, "r") as input_file:
        data = yaml.safe_load(input_file.read())

    
    # Mandatory fields and default values
    assert("validators" in data.keys())
    assert("rippled_image_honest" in data.keys())

    if not "rippled_image_malicious" in data.keys(): data["rippled_image_malicious"] = data["rippled_image_honest"]
    
    for validator in data["validators"]:
        assert("name" in validator.keys())
        assert("public_key" in validator.keys())
        assert("secret_key" in validator.keys())
        assert("token" in validator.keys())
        assert("unl" in validator.keys())
        assert("ip_address" in validator.keys())

        if not "connections" in validator.keys(): validator["connections"] = validator["unl"]
        if not "malicious" in validator.keys(): validator["malicious"] = False
        if not "port" in validator.keys(): validator["port"] = "51235"

    rippled_image_honest, rippled_image_malicious, validators = \
          data["rippled_image_honest"], data["rippled_image_malicious"], data["validators"]

    return rippled_image_honest, rippled_image_malicious, validators


def create_output_folder(output_path: str) -> None:
    # creates folder output_path
    if not os.path.exists(output_path):
        os.mkdir(output_path)


def _get_validator_fixed_ips(validator: dict, validators: list):
    # each validator has section '[ips_fixed]'. This function creates its content and return it as a string
    fixed_ips_string = ""
    validators_list = validator["connections"]   # Store all validators accepted
    for validator in validators:
        if validator["name"] in validators_list:
            fixed_ips_string += f"{validator['name']} {validator['port']}\n"
    return fixed_ips_string


def _wipe_directory(path: str) -> None:
    shutil.rmtree(path)
    os.mkdir(path)


def _map_validator_names_to_pubkeys(validators: list):
    # Create a dictionary from 
    mapping = {}
    try:
        for validator in validators:
            mapping[validator['name']] = validator['public_key']
    except BaseException:
        print("Soemthing went wrong. Are all UNLs defined correctly?")
    return mapping


def create_validator_folders(output_path: str, validators: list) -> None:
    """
    This function creates all needed configuration-files for each validation node.
    It first wipes the output-path and then provisions it again. All information is derived from validators.
    """
    _wipe_directory(output_path)    # Clear output_path before creating files and folders
    validator_to_pubkeys = _map_validator_names_to_pubkeys(validators)
    
    for validator in validators:    
        # Create folders for every validator
        validator_dir = os.path.join(output_path, validator["name"])
        validator_config_path = os.path.join(output_path, validator["name"], "config")
        
        os.mkdir(validator_dir)
        os.mkdir(validator_config_path)

        # Create rippled.cfg file
        with open(os.path.join("templates", "rippled.cfg.temp"), "r") as template_file:
            template_string = template_file.read()

        template_string = template_string.replace("$(validator_token)", validator["token"])
        template_string = template_string.replace("$(validator_port)", validator["port"])
        template_string = template_string.replace("$(validator_fixed_ips)", _get_validator_fixed_ips(validator, validators))
        
        with open(os.path.join(validator_config_path, "rippled.cfg"), "w") as file:
            file.write(template_string)

        # Create validators.cfg (UNLs for each validator)       
        validator_pubkeys_string = "[validators]\n"
        for entry in validator['unl']:
            validator_pubkeys_string += f"    {validator_to_pubkeys[entry]}\n"
        with open(os.path.join(validator_config_path, "validators.txt"), "w") as file:
            file.write(validator_pubkeys_string)


def create_docker_compose_file(validators: list, output_path: str, image_honest: str, image_malicious: str) -> None:
    last_used_ports = {"port1": 8001, "port2": 5006, "port3": 4001, "port4": 9001}  # init these ports
    with open(os.path.join("templates", "docker-compose-validator.yml.temp"), "r") as template_file:
        validator_template_string = template_file.read()
    with open(os.path.join("templates", "docker-compose.yml.temp"), "r") as template_file:
        docker_compose_template_string = template_file.read()

    validators_string = ""
    for validator in validators:
        validator_string: str = validator_template_string
        validator_string = validator_string.replace("$(validator_name)", validator["name"])
        
        validator_string = validator_string.replace("$(validator_port1)", str(last_used_ports["port1"]))
        validator_string = validator_string.replace("$(validator_port2)", str(last_used_ports["port2"]))
        validator_string = validator_string.replace("$(validator_port3)", str(last_used_ports["port3"]))
        validator_string = validator_string.replace("$(validator_port4)", str(last_used_ports["port4"]))

        for port in last_used_ports.keys():
            last_used_ports[port] += 1

        if validator["malicious"]:
            validator_string = validator_string.replace("$(validator_image)", image_malicious)
        else:
            validator_string = validator_string.replace("$(validator_image)", image_honest)
        
        validator_string = validator_string.replace("$(validator_ip_address)", validator["ip_address"])
        
        validators_string += f"{validator_string}\n"
    
    with open(os.path.join(output_path, "docker-compose.yml"), "w") as file:
        docker_compose_string = docker_compose_template_string.replace("$(validators_string)", validators_string)
        file.write(docker_compose_string)


def create_monitoring_file(validators: list, output_path: str) -> None:
    with open(os.path.join(TEMPLATE_PATH, "monitoring.temp"), "r") as temp_file:
        validator_template_string = temp_file.read()
    
    monitoring_string = "#! /bin/bash\n"
    for validator in validators:
        validator_string: str = validator_template_string
        validator_string = validator_string.replace("$(validator_name)", validator["name"])
        monitoring_string += f"\n{validator_string}\n"
    
    with open(os.path.join(output_path, "monitoring.sh"), "w") as write_file:
        write_file.write(monitoring_string)
    
    os.chmod(os.path.join(output_path, "monitoring.sh"), 0o777)


def create_small_monitoring_file(validators: list, output_path: str) -> None:
    with open(os.path.join(TEMPLATE_PATH, "small_monitoring.temp"), "r") as temp_file:
        validator_template_string = temp_file.read()
    
    monitoring_string = "#! /bin/bash\n"
    for validator in validators:
        validator_string: str = validator_template_string
        validator_string = validator_string.replace("$(validator_name)", validator["name"])
        monitoring_string += f"\n{validator_string}\n"
    
    with open(os.path.join(output_path, "small_monitoring.sh"), "w") as write_file:
        write_file.write(monitoring_string)
    
    os.chmod(os.path.join(output_path, "small_monitoring.sh"), 0o777)


def move_files(output_path: str):
    # Move all files in input_path to output_path
    files = os.listdir(FILES_PATH)
    for file_name in files:
        shutil.copy(os.path.join(FILES_PATH, file_name), output_path)


@argh.arg('input_path',help="Input path to validator-information")
@argh.arg('output_path',help="Path to output validator-configs and file structure")
def main(input_path, output_path):
    image_honest, image_malicious, validators = read_data_from_input(input_path)
    create_output_folder(output_path)
    create_validator_folders(output_path, validators)
    create_docker_compose_file(validators, output_path, image_honest, image_malicious)
    create_monitoring_file(validators, output_path)
    create_small_monitoring_file(validators, output_path)
    move_files(output_path)


if __name__=="__main__":
    try:
        argh.dispatch_command(main)
    except BaseException as err:
        print(f"Something went wrong: {err}")
