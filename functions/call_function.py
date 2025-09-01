def call_function(function_call_part, verbose=False):
    function=function_call_part
    working_dir="./calculator"
    for part in function:
        print(part)
    if verbose:
        print(f"Calling function: {function.name}({function.args})")
    else:
        print(f" - Calling function: {function.name}")

    #result=f'{function.name}({working_dir}, **{(str(function.args))})'
    #print(f'result: {result}')
    try:
        #response = f'{result}'
        #response
        result=function.name(working_dir, **function.args)
        print(result)
    except Exception as e:
        print(type(function.name))
        return f'Error: {e}'
