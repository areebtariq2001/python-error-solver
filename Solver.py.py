#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import sys, io, traceback, re

error_history = []
current_fix = ""

def get_auto_fix(code, error_type, line_no):
    if error_type == "IndexError":
        return f"# Fix: Index check lagao\nif len(x) > {line_no}:\n {code}\nelse:\n print('List choti hai')"
    elif error_type == "NameError":
        var = re.search(r"name '(\\w+)' is not defined", str(code))
        v = var.group(1) if var else "variable"
        return f"{v} = None # Fix: Define kar diya\n{code}"
    elif error_type == "ZeroDivisionError":
        return f"# Fix: Zero check\na = 10\nb = 0\nresult = a / b if b!=0 else 0\nprint(result)"
    elif error_type == "KeyError":
        return code.replace('[', '.get(').replace(']', ', \"Not Found\")')
    elif error_type == "TypeError" and '+' in code:
        return f"# Fix: str() use karo\n{re.sub(r'(\\w+)', r'str(\\1)', code)}"
    else:
        return f"# Manual fix chahiye\n{code}"

def samjhao_error_v3(error_type, error_msg):
    fixes = {
        "ZeroDivisionError": "0 se divide nahi hota. 'if x!=0:' laga do",
        "NameError": "Variable banaya hi nahi. 'xyz = 0' likh do pehle",
        "SyntaxError": "Bracket ya colon miss hai. Line check karo",
        "TypeError": "str() ya int() se type same karo",
        "IndexError": "List choti hai. len(list) se size check karo",
        "KeyError": "Key nahi mili. dict.get('key', 'default') use karo",
        "ValueError": "Galat value di hai. Sahi format mein do",
        "IndentationError": "Space ka issue hai. Tab/Space same rakho"
    }
    return fixes.get(error_type, "Google pe 'python "+error_type+"' search karo")

code_box = widgets.Textarea(value='x = [1,2]\nprint(x[5])', description='Code:', layout=widgets.Layout(width='95%', height='100px'))
upload = widgets.FileUpload(description="File Chuno", multiple=False)
check_btn = widgets.Button(description="Check Karo", button_style='danger', icon='bug')
history_btn = widgets.Button(description="History Dekho", button_style='info', icon='history')
autofix_btn = widgets.Button(description="Auto-Fix Karo", button_style='primary', icon='magic', disabled=True)
btn_box = widgets.HBox([check_btn, history_btn, autofix_btn])
output = widgets.Output()
fix_box = widgets.Textarea(description='Fixed Code:', layout=widgets.Layout(width='95%', height='80px'), disabled=True)

def show_history(b):
    with output:
        clear_output()
        print("=== ERROR HISTORY ===")
        if not error_history: print("Abhi tak koi error nahi")
        else:
            for i, err in enumerate(error_history, 1): print(f"{i}. {err}")

def apply_autofix(b):
    global current_fix
    fix_box.value = current_fix
    fix_box.disabled = False
    with output: clear_output(); print("🔧 Auto-Fixed code neeche daal diya! Copy kar lo")

def check_error(b):
    global current_fix
    with output:
        clear_output()
        fix_box.value = ""; fix_box.disabled = True
        autofix_btn.disabled = True
        code = ""
        if upload.value:
            try:
                f = list(upload.value.values())[0]
                code = f['content'].decode('utf-8')
                print(f"File: {f['metadata']['name']}")
            except: print("File nahi padh paya"); return
        elif code_box.value.strip():
            code = code_box.value; print("Pasted Code Check:")
        else: print("Kuch to daal bhai"); return
        print("-" * 40)
        try:
            exec(code, {}); print("✅ SAB SAHI HAI! Koi error nahi")
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line = tb[-1].lineno if tb else "?"
            err_type = type(e).__name__; err_msg = str(e)
            print("❌ ERROR PAKDA GAYA!")
            print(f"📍 Line Number: {line}\n🐛 Error: {err_type}\n💻 Detail: {err_msg}")
            print("-" * 40)
            fix = samjhao_error_v3(err_type, err_msg)
            current_fix = get_auto_fix(code, err_type, line)
            print(f"💡 Asaan Zuban: {fix}\n\n🔧 Auto-Fix Suggestion Ready!")
            autofix_btn.disabled = False
            error_history.insert(0, f"Line {line}: {err_type} - {err_msg[:40]}")
            if len(error_history) > 5: error_history.pop()

check_btn.on_click(check_error)
history_btn.on_click(show_history)
autofix_btn.on_click(apply_autofix)

display(HTML("<h2>🔥 Python Error Solver v3.0 - Notebook Edition 🔥</h2>"))
display(code_box); display(upload); display(btn_box); display(output); display(fix_box)


# In[ ]:




