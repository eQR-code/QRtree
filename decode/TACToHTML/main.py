from .parser import Parser
from .scanner import Scanner
from .three_address_code import Instruction, ThreeAddressCode, ComparativeOperand
import argparse

def to_html(file, code):
    style = """
    div[data-line] {
        display: none;
    }
    div[data-line][data-executed] {
        display: block;
    }
    """

    script = """
    const execute_event = new Event('execute');
    let cur_line = 0;
    let last_input = null;

    const cmp_table = {
        1: (a, b) => a < b,
        2: (a, b) => a <= b,
        3: (a, b) => a > b,
        4: (a, b) => a >= b,
        5: (a, b) => a == b,
        6: (a, b) => a != b
    }

    function execute() {
        let elements = document.querySelectorAll(`div[data-line='${cur_line}']`);
        if (elements != null) {
            for (let line of elements) {
                let ex = new execute_event.constructor(execute_event.type, execute_event);
                line.dispatchEvent(ex);
            }
        }
    }

    function next() {
        cur_line++;
        execute();
    }

    function goto(line) {
        cur_line = line;
        execute();
    }

    function if_true(line, goto_line) {
        let current = document.querySelector(`div[data-line='${line}']`);
        let n = current.nextSibling;
        while (n.dataset.type == 'if' || n.dataset.type == 'else') {
            n.getElementsByTagName("button")[0].disabled = true;
            n = n.nextSibling;
        }
        n = current.previousSibling;
        while (n.dataset.type == 'if' || n.dataset.type == 'else') {
            n.getElementsByTagName("button")[0].disabled = true;
            n = n.previousSibling;
        }
        current.getElementsByTagName("button")[0].disabled = true;
        goto(goto_line);
    }

    function inputs_submit() {
        let current = document.querySelector(`div[data-line='${cur_line}']`);
        current.getElementsByTagName("button")[0].disabled = true;
        current.getElementsByTagName("input")[0].disabled = true;
        next();
    }

    (function () {
        for (let line of document.querySelectorAll("div[data-line][data-type='print'], div[data-line][data-type='input']")) {
            line.addEventListener("execute", (event) => {
                if (!event.currentTarget.dataset.executed) {
                    next();
                    line.dataset.executed = true;
                }
            });
        }
        for (let line of document.querySelectorAll("div[data-line][data-type='inputs'], div[data-line][data-type='else'], div[data-line][data-type='printex']")) {
            line.addEventListener("execute", (event) => {
                if (!event.currentTarget.dataset.executed) {
                    line.dataset.executed = true;
                }
            });
        }
        for (let line of document.querySelectorAll("div[data-line][data-type='if']")) {
            line.addEventListener("execute", (event) => {
                if (!event.currentTarget.dataset.executed) {
                    let next_if = event.currentTarget.nextSibling;
                    if (next_if.dataset.type == 'if') {
                        next();
                    }
                    line.dataset.executed = true;
                }
            });
        }
        for (let line of document.querySelectorAll("div[data-line][data-type='ifc']")) {
            line.addEventListener("execute", (event) => {
                if (!event.currentTarget.dataset.executed) {
                    let prev = event.currentTarget.previousSibling;
                    while (prev != null && prev.dataset.type != 'inputs') {
                        prev = prev.previousSibling;
                    }
                    let input = parseFloat(prev.getElementsByTagName("input")[0].value);
                    let cmp = event.currentTarget.dataset.par1Cmp;
                    let val = parseFloat(event.currentTarget.dataset.par1Val);
                    if (Number.isInteger(val)) {
                        input = parseInt(input);
                    }

                    if (cmp_table[cmp](input, val)) {
                        goto(parseInt(event.currentTarget.dataset.par2));
                    } else {
                        next();
                    }
                    
                    line.dataset.executed = true;
                }
            });
        }
        for (let line of document.querySelectorAll("div[data-line][data-type='goto']")) {
            line.addEventListener("execute", (event) => {
                if (!event.currentTarget.dataset.executed) {
                    let par1 = parseInt(line.dataset.par1);
                    goto(par1);
                    line.dataset.executed = true;
                }
            });
        }
        execute();
    })();
    """
    return f"""<!DOCTYPE HTML>
<html>
    <head>
        <title>{file}</title>
        <meta charset=\"utf-8\"/>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
        <style>
            {style}
        </style>
    </head>
    <body>
        <div class=\"container-fluid\">
            <div class=\"row\">
                <h1>{file}</h1>
            </div>
            <main class=\"row\">
                {code_to_html(code)}
            </main>
        </div>
        <script>
            {script}
        </script>
    </body>
</html>"""

def code_to_html(code):
    ret = ""

    for i, instruction in enumerate(code):
        ret += instruction_map[instruction.instruction](i, instruction)
        if instruction.instruction == Instruction.IF and code[i+1].instruction != Instruction.GOTO and code[i+1].instruction != Instruction.IF:
            ret += f"<div class=\"col-auto\" data-line=\"{i}\" data-type=\"else\"><button type=\"button\" class=\"btn btn-sm btn-secondary\" onclick=\"if_true({i}, {i + 1})\">Altro</button></div>"
        
    return ret

def input_to_html(line, input):
    if isinstance(input.par1, int):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"input\"><h3>Look at reference {input.par1}</h3></div>"
    elif isinstance(input.par1, str):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"input\"><h3>{input.par1}</h3></div>"
    else:
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"input\"><h3>?</h3></div>"

def inputs_to_html(line, inputs):
    if isinstance(inputs.par1, int):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"inputs\"><h3>Look at reference {inputs.par1}</h3><div class=\"row\"><div class=\"col-lg-11 col-10\"><input type=\"text\" class=\"form-control\" /></div><div class=\"col-lg-1 col-2\"><button type=\"button\" class=\"btn btn-sm btn-primary\" onclick=\"inputs_submit()\">Ok</button></div></div></div>"
    elif isinstance(inputs.par1, str):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"inputs\"><h3>{inputs.par1}</h3><div class=\"row\"><div class=\"col-lg-11 col-10\"><input type=\"text\" class=\"form-control\" /></div><div class=\"col-lg-1 col-2\"><button type=\"button\" class=\"btn btn-sm btn-primary\" onclick=\"inputs_submit()\">Ok</button></div></div></div>"
    else:
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"inputs\"><h3>?</h3><div class=\"row\"><div class=\"col-lg-11 col-10\"><input type=\"text\" class=\"form-control\" /></div><div class=\"col-lg-1 col-2\"><button type=\"button\" class=\"btn btn-sm btn-primary\" onclick=\"inputs_submit()\">Ok</button></div></div></div>"

def print_to_html(line, print):
    if isinstance(print.par1, int):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"print\"><h3>Look at reference {print.par1}</h3></div>"
    elif isinstance(print.par1, str):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"print\"><h3>{print.par1}</h3></div>"
    else:
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"print\"><h3>?</h3></div>"

def if_to_html(line, _if):
    return f"<div class=\"col-auto\" data-line=\"{line}\" data-type=\"if\"><button type=\"button\" class=\"btn btn-sm btn-primary\" onclick=\"if_true({line}, {_if.par2})\">{_if.par1}</button></div>"

def ifc_to_html(line, _ifc):
    return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"ifc\" data-par1-cmp=\"{_ifc.par1[0].value}\" data-par1-val=\"{_ifc.par1[1]}\" data-par2=\"{_ifc.par2}\"></div>"

def goto_to_html(line, goto):
    return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"goto\" data-par1=\"{goto.par1}\"></div>"

def printex_to_html(line, printex):
    if isinstance(printex.par1, int):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"printex\"><h3>Look at reference {printex.par1}</h3></div>"
    elif isinstance(printex.par1, str):
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"printex\"><h3>{printex.par1}</h3></div>"
    else:
        return f"<div class=\"col-12\" data-line=\"{line}\" data-type=\"printex\"><h3>?</h3></div>"

instruction_map = {
    Instruction.INPUT: input_to_html,
    Instruction.INPUTS: inputs_to_html,
    Instruction.PRINT: print_to_html,
    Instruction.IF: if_to_html,
    Instruction.IFC: ifc_to_html,
    Instruction.GOTO: goto_to_html,
    Instruction.PRINTEX: printex_to_html
}

def decode(file, debug):
    s = Scanner(debug)
    p = Parser(s, debug)
    file_content = None
    with open(f"output.txt", 'r') as f:
        file_content = f.read()

    code = p.parse(file_content)
    html = to_html(file, code)
    with open(f"{file}", 'w') as f:
            f.write(html)
    
    return code

def main(args):
    for file in args.files:
        code = decode(file, args.debug)

        if args.verbose:
            print(f"Line  |  {'Instruction': <{ThreeAddressCode.COLUMN_WIDTH}}|  {'Arg1': <{ThreeAddressCode.COLUMN_WIDTH}}|  {'Arg2': <{ThreeAddressCode.COLUMN_WIDTH}}")
            print("-" * (7 + (ThreeAddressCode.COLUMN_WIDTH + 3) * 3))
            for (i, line) in enumerate(code):
                print(f"({i:03}) |  {line}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="QRscript transcompiler to html page with interpreter")
    parser.add_argument("files", metavar="file", type=str, nargs='+')
    parser.add_argument("-d", "--debug", action='store_true', help="Prints the debug output of parser and scanner")
    parser.add_argument("-v", "--verbose", action='store_true', help="Prints the output three-address code")
    args = parser.parse_args()
    main(args)