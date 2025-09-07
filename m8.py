# ⚡ M8-FK Interpreter: FINAL EDITION+ ⚡

tape = [0] * 30000
ptr = 0  
def run_m8fk(code):
    global ptr, tape
    i = 0
    loop_stack = []

    while i < len(code):
        line = code[i].strip()

        # 🛑 Skip blank lines and full-line comments

        if line.startswith('#') or line == '':
             i += 1
             continue
        line = line.upper()

        if line.startswith('INC'):
            try:
                n = int(line.split('~')[1])
            except:
                print(f'❌ Invalid INC format at line {i + 1}')
                return
            tape[ptr] = (tape[ptr] + n) % 256

        elif line == 'DUMP':
           	 print('\n TAPE DUMP:', tape[:40])


        elif line.startswith('DEC'):
            try:
                n = int(line.split('~')[1])
            except:
                print(f'❌ Invalid DEC format at line {i + 1}')
                return
            tape[ptr] = (tape[ptr] - n) % 256

        elif line == 'RIGHT':
            ptr += 1
            if ptr >= len(tape):
                ptr = 0  # wrap around

        elif line == 'LEFT':
            ptr -= 1
            if ptr < 0:
                ptr = len(tape) - 1  # wrap around

        elif line == 'PRNT':
            print(chr(tape[ptr]), end='')

        elif line == 'NL':
            print()  # newline

        elif line == 'READ':
            try:
                tape[ptr] = ord(input("Input: ")[0])
            except:
                tape[ptr] = 0

        elif line == 'CLR':
            tape = [0] * 30000
            ptr = 0

        elif line.startswith('GOTO'):
            try:
                goto_line = int(line.split('~')[1]) - 1
                if 0 <= goto_line < len(code):
                    i = goto_line
                    continue
                else:
                    print(f'❌ GOTO line {goto_line + 1} out of range')
                    return
            except:
                print(f'❌ Invalid GOTO format at line {i + 1}')
                return

        elif line == 'LOOP':
            if tape[ptr] == 0:
                open_loops = 1
                while open_loops > 0:
                    i += 1
                    if i >= len(code):
                        print('❌ LOOP without END')
                        return
                    if code[i].strip().upper() == 'LOOP':
                        open_loops += 1
                    elif code[i].strip().upper() == 'END':
                        open_loops -= 1
            else:
                loop_stack.append(i)

        elif line == 'END':
            if not loop_stack:
                print('❌ END without LOOP')
                return
            i = loop_stack[-1] - 1
            loop_stack.pop()

        else:
            print(f'❌ Unknown command: {line} (line {i + 1})')
            return

        i += 1

if __name__ == "__main__":
    file = input("Enter .m8 file: ")
    try:
        with open(file) as f:
            code = f.readlines()
        run_m8fk(code)
    except FileNotFoundError:
        print("❌ File not found")
