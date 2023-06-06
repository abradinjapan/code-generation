# generate a short namespace
def generate_c_short_namespace(global_namespace, function_name):
    return global_namespace + "__" + function_name

# generate a long namespace
def generate_c_long_namespace(global_namespace, typespace, function_name):
    return global_namespace + "__" + typespace + "__" + function_name

# generate a short register name
def generate_c_short_register(global_namespace, function_name, register_name):
    return generate_c_short_namespace(global_namespace, function_name) + "__" + register_name

# generate a long register name
def generate_c_long_register(global_namespace, typespace, function_name, register_name):
    return generate_c_long_namespace(global_namespace, typespace, function_name) + "__" + register_name

# generate a function coder
def generate_c_code_function(global_namespace, function_name):
    return global_namespace + "__code__" + function_name

# generate an offset pointer name
def generate_offsets_name(global_namespace):
    return global_namespace.lower() + "_offsets"

# generate c code for a forge function
def generate_forge_c_function(global_namespace, function_name, variables, inputs, outputs):
    # setup variables
    output = ""
    preserve_start = False

    # write comment header
    output += "/* " + function_name[0].upper() + function_name[1:] + " */\n"

    # generate registers header
    output += "// register types\n"

    # generate enum
    output += "typedef enum " + generate_c_short_namespace(global_namespace, function_name) + " {\n"

    # generate preserve start
    output += "\t// preserve start\n"
    output += "\t" + generate_c_short_register(global_namespace, function_name, "preserve__START") + " = " + generate_c_long_register("ANVIL", "srt", "start", "workspace") + ",\n"

    # generate variables comment
    output += "\n\t// variables\n"

    # counter
    i = 0

    # generate input variables
    while i < len(inputs):
        # write variables
        output += "\t" + generate_c_short_register(global_namespace, function_name, inputs[i])

        # if first item in list
        if i == 0 and preserve_start == False:
            # write preserve start
            output += " = " + generate_c_short_register(global_namespace, function_name, "preserve__START")

            # first input was found
            preserve_start = True
        
        # finish line
        output += ",\n"

        # next input
        i += 1

    # counter
    i = 0

    # generate output variables
    while i < len(outputs):
        # write variables
        output += "\t" + generate_c_short_register(global_namespace, function_name, outputs[i])

        # if first item in list
        if i == 0 and preserve_start == False:
            # write preserve start
            output += " = " + generate_c_short_register(global_namespace, function_name, "preserve__START")

            # first input was found
            preserve_start = True

        # finish line
        output += ",\n"

        # next input
        i += 1

    # counter
    i = 0

    # generate variables
    while i < len(variables):
        # write variables
        output += "\t" + generate_c_short_register(global_namespace, function_name, variables[i])

        # if first item in list
        if i == 0 and preserve_start == False:
            # write preserve start
            output += " = " + generate_c_short_register(global_namespace, function_name, "preserve__START")

            # first input was found
            preserve_start = True
        
        # finish line
        output += ",\n"

        # next input
        i += 1

    # generate preserve end
    output += "\n\t// preserve end\n"
    output += "\t" + generate_c_short_register(global_namespace, function_name, "preserve__END") + ",\n\n"

    # generate inputs banner
    output += "\t// inputs\n"

    # counter
    i = 0

    # generate inputs
    while i < len(inputs):
        # write inputs
        output += "\t" + generate_c_long_register(global_namespace, function_name, "input", inputs[i])

        # if first item in list
        if i == 0:
            output += " = " + generate_c_long_register("ANVIL", "srt", "start", "function_io")
        
        # finish line
        output += ",\n"

        # next input
        i += 1

    # generate outputs banner
    output += "\n\t// outputs\n"

    # counter
    i = 0

    # generate outputs
    while i < len(outputs):
        # write outputs
        output += "\t" + generate_c_long_register(global_namespace, function_name, "output", outputs[i])

        # if first item in list
        if i == 0:
            output += " = " + generate_c_long_register("ANVIL", "srt", "start", "function_io")
        
        # finish line
        output += ",\n"

        # next input
        i += 1
    
    # finish variables
    output += "} " + generate_c_short_namespace(global_namespace, function_name) + ";\n\n"

    # generate caller
    output += "// call function\n"
    output += "void " + generate_c_long_register(global_namespace, "code", "call", function_name) + "(ANVIL__workspace* workspace, " + global_namespace + "__offsets* " + generate_offsets_name(global_namespace) + ", ANVIL__flag_ID flag"

    # generate inputs
    for input_iterator in inputs:
        # generate input
        output += ", ANVIL__register_ID input__" + input_iterator
    
    # generate outputs
    for output_iterator in outputs:
        # generate input
        output += ", ANVIL__register_ID output__" + output_iterator
    
    # finish header
    output += ") {\n"

    # start inputs
    output += "\t// pass inputs\n"

    # generate parameter input passes
    for input_iterator in inputs:
        # generate input passer
        output += "\tANVIL__code__register_to_register(workspace, flag, input__" + input_iterator + ", " + generate_c_long_register(global_namespace, function_name, "input", input_iterator) + ");\n"

    # call function
    output += "\n\t// call function\n"
    output += "\tANVIL__code__call__static(workspace, flag, (*" + generate_offsets_name(global_namespace) + ").offsets[" + generate_c_long_register(global_namespace, "ot", function_name, "start") + "]);\n\n"
    output += "\t// pass outputs\n"

    # generate parameter output passes
    for output_iterator in outputs:
        # generate input passer
        output += "\tANVIL__code__register_to_register(workspace, flag, " + generate_c_long_register(global_namespace, function_name, "output", output_iterator) + ", output__" + output_iterator + ");\n"

    # finish call
    output += "}\n\n"

    # generate function
    output += "// build function\n"
    output += "void " + generate_c_code_function(global_namespace, function_name) + "(ANVIL__workspace* workspace, " + global_namespace + "__offsets* " + generate_offsets_name(global_namespace) + ") {\n"
    output += "\t// setup function offset\n"
    output += "\t(*" + generate_offsets_name(global_namespace) + ").offsets[" + generate_c_long_register(global_namespace, "ot", function_name, "start") + "] = ANVIL__get__offset(workspace);\n\n"
    output += "\t// setup function prologue\n"
    output += "\tANVIL__code__preserve_workspace(workspace, ANVIL__sft__always_run, " + generate_c_short_register(global_namespace, function_name, "preserve__START") + ", " + generate_c_short_register(global_namespace, function_name, "preserve__END") + ");\n\n"
    output += "\t// get inputs\n"

    # generate function input getters
    for input in inputs:
        # create input getter
        output += "\tANVIL__code__register_to_register(workspace, ANVIL__sft__always_run, " + generate_c_long_register(global_namespace, function_name, "input", input) + ", " + generate_c_short_register(global_namespace, function_name, input) + ");\n"
    
    # generate start of code
    output += "\n\t// code here\n\n\n"

    # generate start of output setters
    output += "\t// setup outputs\n"

    # generate function output setters
    for output_iterator in outputs:
        # create output setter
        output += "\tANVIL__code__register_to_register(workspace, ANVIL__sft__always_run, " + generate_c_short_register(global_namespace, function_name, output_iterator) + ", " + generate_c_long_register(global_namespace, function_name, "output", output_iterator) + ");\n"
    
    # next line
    output += "\n"

    # generate function end
    output += "\t// setup function epilogue\n"
    output += "\tANVIL__code__restore_workspace(workspace, ANVIL__sft__always_run, " + generate_c_short_register(global_namespace, function_name, "preserve__START") + ", " + generate_c_short_register(global_namespace, function_name, "preserve__END") + ");\n\n"

    # generate return
    output += "\t// return to caller\n"
    output += "\tANVIL__code__jump__explicit(workspace, ANVIL__sft__always_run, ANVIL__srt__return_address);\n\n"
    output += "\treturn;\n"
    output += "}\n\n"

    return output

# get a list of inputs
def get_list(list_name):
    # tell user this is a list
    print("List Type - " + list_name)
    print("Please enter each name and enter a blank name to stop adding names.")

    # setup output
    output = []

    # get inputs
    while True:
        # get string
        data = input("Next name: ")

        # if empty, exit
        if data == "":
            return output

        # add name
        output.append(data)

# entry point
def generate():
    # inform of generation start
    print("Generating code...\n")

    # setup variables
    global_namespace = input("Please select a global namespace: ")
    function_name = input("Please choose your function's name: ")
    variables = get_list("Variables")
    inputs = get_list("Inputs")
    outputs = get_list("Outputs")

    # call function
    code = generate_forge_c_function(global_namespace, function_name, variables, inputs, outputs)

    # print result
    print(code)

    pass

generate()
