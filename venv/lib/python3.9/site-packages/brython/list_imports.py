imports = []
with open("imports.txt") as f:
    for line in f:
        if line.startswith("sympy/"):
            module = (line.strip().replace("/", "."))
            if module.endswith(".__init__.py"):
                module = module[:-len(".__init__.py")]
            elif module.endswith(".py"):
                module = module[:-3]
            imports.append(module)
        elif '404' in line:
            imports.pop()

print("imports", imports, len(imports))