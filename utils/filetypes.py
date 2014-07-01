# File containing the Meta interface to add new languages.
# Please do not change any original code. To add new languages please follow the instruction given in the comments below and the documentation.

import os, pickle

'''
This is the array containing the languages supported by the system. To add a new language just add the name of the language to this array.
Once that is done, please read up the comments for each of the arrays below, add make suitable additions.
'''
LANGUAGES = [
            'C++',
            'C',
            'Java',
            'Python',
            'Bash',
]

'''
This is the array containing the languages the need compilation. If your language is a compiled language, then add it here. Please note that
the name should be the same as added in the LANGUAGES array.
'''
COMPILED_LANGUAGES = ['C',
                      'C++',
                      'Java',
]

'''
This is the array containing the languages that are just interpreted. If your language is an interpreted language, then add it here. Please note that
the name should be the same as added in the LANGUAGES array. 
NOTE: Languages that compile to a binary file (C/C++) need not be added here. 
'''
INTERPRETED_LANGUAGES = ['Python',
                         'Bash', 
                         'Java',
]

'''
This is the dictionary that maps the languages to the compilers used to compile them. If your language is a compiled language, then add the language
name and the compiler to be used here. Please note that the name of the language should be the same as added in the LANGUAGES array.
NOTE: The compiler should be installed on the system running the server.
'''
COMPILERS = {
            'C++': 'g++',
            'C': 'gcc',
            'Java': 'javac',
}

'''
This is the dictionary that maps the interpreted languages to the interpreters used to interpret them. If your language is an interpreted language, 
then add the language name and the interpeter to be used here. Please note that the name of the language should be the same as added in the LANGUAGES 
array. 
NOTE: The interpreter should be installed on the system running the server.
NOTE: For compiled languages, add the interpreter used to interpret the byte/object code. If the final object code is in the form of a binary file,
the dont add anything (Ex: C/C++).
'''
INTERPRETERS = {
            'Java' : 'java',
            'Python': 'python',
            'Bash': 'bash',
}

'''
This is the dictionary that maps the compiler names to the list of file extensions that the compilers recognizes/are valid. If your language is a
compiled language, then add the compiler name and the list of valid extensions. Please note that the name of the compiler should be the same as added 
in the COMPILERS dictionary.
NOTE: When creating assignments, the solution files to be uploaded are cross checked with this list. So please ensure that you have covered all valid
      extensions.
'''
VALID_EXTENSIONS_COMPILERS = {
            'g++': ['.cpp', '.h', '.hpp'],
            'gcc': ['.c', '.h'],
            'javac': ['.java'],
}

'''
This is the dictionary that maps the interpreter names to the list of file extensions that the interpreter recognizes/are valid. If your language is a
interpreted language, then add the interpreter name and the list of valid extensions. Please note that the name of the interpreter should be the same 
as added in the INTERPRETERS dictionary.
NOTE: When creating assignments, the extensions of the solution files to be uploaded are cross checked with this list. So please ensure that you have 
      covered all valid extensions.
'''
VALID_EXTENSIONS_INTERPRETERS = {
            'java': ['.class', '.java', '.jar', ''],
            'python': ['.py'],
            'bash': ['.sh'],
}

'''
This is the dictionary that maps the language names to the list of file extensions of the intermediate file created during the 
compilation/interpretation process. Add the language name and the list of valid extensions. Please note that the name of the laugnage should be the same 
as added in the LANGUAGES array.
NOTE: This array is used to find the intermediate files (by their extensions) to delete them and isolate the output files. Please add all possible extensions.
'''
INTERMEDIATE_FILES_EXTENSIONS = {
            'C':['.exe'],
            'C++': ['.exe'],
            'Java': ['.class', '.jar'],
            'Python': ['.pyc'],
            'Bash':[]
}

# Function to find if a language needs compilation or not. Checks the COMPILED_LANGUAGES array to find out the same.
# Takes as input the language name as given in the LANGUAGES array.
def compile_required(language):
    if language in COMPILED_LANGUAGES:
        return True
    else:
        return False

'''
Function to find if the execution process needs to retrieve execution command from the database or not. While adding a new language, make sure 
to add the condition for the new language as needed.
'''
# Takes as input the language name as given in the LANGUAGES array.
def execution_command_required(language):
    if language == 'C' or language == 'C++':
        return False
    else:
        return True

# Function to retrieve compiler used to compile the language. Make sure that every compiled language has an entry in the COMPILERS dictionary.
# Takes as input the language name as given in the LANGUAGES array.
def get_compiler_name(lang):
    return COMPILERS[lang]

# Function to retrieve interpreter used to interpret the language. Make sure that every interpreted language has an entry in the INTERPRETERS 
# dictionary. In case the object code is a binary file then no need to add anything to the INTERPRETERS dictionary.
# Takes as input the language name as given in the LANGUAGES array.
def get_interpreter_name(lang):
    return INTERPRETERS[lang]

# Function to retrieve file extensions that are recognized by the compiler and the interpreter of the language. This function is called to cross
# check the files to be uploaded as solution code with the supported extensions for the language.
# Takes as input the language name as given in the LANGUAGES array.
def get_extension(lang):
    extensions = []
    if lang in COMPILED_LANGUAGES:
        extensions += VALID_EXTENSIONS_COMPILERS[get_compiler_name(lang)]
    elif lang in INTERPRETED_LANGUAGES:
        extensions += VALID_EXTENSIONS_INTERPRETERS[get_interpreter_name(lang)]
    return extensions

# Function retrieve the language category of the language given as input. The categories are as follows.
# 0 - Languages which do not need execution command to be given by the user. The execution command is constructed according to the language
#    Ex: C/C++ uses the executable name as the execution command.
# 1 - Language which needs the compilation and interpreter command to be given by the user. Languages like Java.
# 2 - Language which needs only the execution command to be given by the user. The language either does not compile or the compilation command is 
#    constructed implicitly.

def language_category(lang):
    if lang == 'C' or lang == 'C++':
        return 0
    elif lang in COMPILED_LANGUAGES:
        return 1
    elif lang in INTERPRETED_LANGUAGES:
        return 2
        
# Function to check if the given filename is valid for the given compiler/interpreter. It uses the VALID_EXTENSIONS_* arrays do the same.
# NOTE: Only 2 of language, compiler and interpreter are supposed to given as arguments.
# Takes as input the filename, language of the assignment, compiler to be used and the interpreter to be used.
def is_valid(filename, lang=None, compiler=None, interpreter=None):
    if lang and compiler:
        raise ValueError("Provide exactly one arguments 'lang' or 'compiler'. Provided both.")
    if lang and interpreter:
        raise ValueError("Provide exactly one arguments 'lang' or 'interpreter'. Provided both.")
    if interpreter and compiler:
        raise ValueError("Provide exactly one arguments 'compiler' or 'interpreter'. Provided both.")
    if lang:
        extensions = get_extension(lang)

    if compiler:
        extensions = VALID_EXTENSIONS_COMPILERS[compiler]

    if interpreter:
        extensions = VALID_EXTENSIONS_INTERPRETERS[interpreter]

    _, ext = os.path.splitext(filename)
    return (ext in extensions) # Returns True OR False

# Function to get the compilation command of the program/section. For C/C++, the function returns the command that creates the appropriate executable.
# For the rest of the languages the function returns the compilation command as given when creating the section if the language needs to be compiled.
# Otherwise the function returns an empty string.
# Takes as input the section/program object for which the compilation command is needed.
def get_compilation_command(program):
    if program.language == 'C' or program.language == 'C++':
        return " ".join(pickle.loads(program.compiler_command)) + " -o " + "exe_" + str(program.id)
    elif program.compiler_command:
        return " ".join(pickle.loads(program.compiler_command))
    else:
        return ""

# Function to get the execution command of the program/section. For C/C++, the function returns the command as executing the binary file.
# For the rest of the languages the function returns the execution command as given when creating the section.
# Takes as input the section/program object for which the execution command is needed.
def get_execution_command(program):
    if program.language == 'C' or program.language == 'C++':
        return "./" + "exe_" + str(program.id)
    elif program.language in INTERPRETED_LANGUAGES:
        return " ".join(pickle.loads(program.execution_command))

# Function to check if the given filename is an intermediate file w.r.t to the language. 
# Takes as input the filename to be checked, the section of which the file belongs to (needed for check on binary files), and the language 
# of the assignment (as given in the LANGUAGE array).
def is_intermediate_files(filename, program, language):
    if program.language == 'C' or program.language == 'C++':
        return (filename == "exe_"+ str(program.id))
    else:
        _, ext = os.path.splitext(filename)
        return (ext in INTERMEDIATE_FILES_EXTENSIONS[language])

# Function to retrieve the files used in the interpreter command.
# Takes as input the section/program whose files are needed.
def get_execution_command_files(program):
    if program.execution_command:
        return pickle.loads(program.execution_command)[2].split()
    else:
        return []

# Function to retrieve the files used during the compilation process.
# Takes as input the section/program whose files are needed.
def get_compilation_command_files(program):
    if program.compilation_command:
        return pickle.loads(program.compilation_command)[2].split()
    else:
        return []
