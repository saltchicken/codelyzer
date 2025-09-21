from code_context import CodeContext

cc = CodeContext("../code_context/", [".py"])
output_parts = []

output_parts.append(cc.get_full_context())

final_output = "\n\n".join(output_parts).strip()
print(final_output)

print(cc.file_paths)
