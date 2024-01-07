import json, datetime, sys, os
from openai import OpenAI

def md2json(relative_path, base_path):
    # Open and read the markdown file
    with open(base_path+relative_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Initialize variables to store the parsed data
    data = {"messages": []}
    current_role = ""
    current_content = ""

    # A set of allowed roles in lowercase
    allowed_roles = {"user", "assistant", "system"}

    # Iterate through each line in the file
    for line in lines:
        # Check if the line is a role indicator
        if line.startswith("# 𝍖"):
            role = line.strip().split(" ")[1][1:].lower()  # Convert role to lowercase
            # Check if the role is one of the allowed roles
            if role in allowed_roles:
                # If there's existing content, add it to data before changing role
                if current_content:
                    data["messages"].append({
                        "role": current_role,
                        "content": current_content.strip()
                    })
                    current_content = ""  # Reset content for new role
                current_role = role
        # Otherwise, accumulate the message content
        else:
            current_content += line

    # Add the last accumulated content to data if it exists
    if current_content:
        data["messages"].append({
            "role": current_role,
            "content": current_content.strip()
        })

    return data

def json2md(json_data):
    # Initialize an empty string to store the markdown content
    markdown_content = ""

    # A set of allowed roles
    allowed_roles = {"user", "assistant", "system"}

    # Iterate through each message in the JSON
    for message in json_data['messages']:
        # Check if the role is one of the allowed roles
        if message['role'].lower() in allowed_roles:
            # Add the role with the prefix
            markdown_content += f"# 𝍖{message['role']}\n"
        # Add the content with a newline after
        markdown_content += f"{message['content']}\n\n"

    return markdown_content.strip()

def main(relative_path,base_path):
    # Convert markdown to JSON
    json_data = md2json(relative_path, base_path)
    json_folder_path = ".llmjsons\\convert_outputs\\"

    # Save the JSON data to a file with a timestamp
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    safe_filename = relative_path.replace("\\", "_").replace(":", "-")  # Replace backslashes and colons

    json_filename = os.path.join(base_path, json_folder_path, f"{current_time}-{safe_filename}-before.json")
    with open(json_filename, "w", encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    # Convert json_data to the desired string format
    # ... Your code for formatting ...

    # Uncomment the following if you want to use OpenAI API
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
    completion_json = json_data
    completion_json = {
        "messages": [message for message in json_data["messages"] if message["role"] != ""]
    }
    #print(completion_json)
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=completion_json["messages"],
        temperature=0,#0.7,
    )
    completion_message = str(completion.choices[0].message.content)
    #print(completion_message)
    json_data["messages"].append({
        "role": "assistant",
        "content": completion_message
    })

    # Save the JSON data to a file with a timestamp
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    json_filename = os.path.join(base_path, json_folder_path, f"{current_time}-{safe_filename}-after.json")
    with open(json_filename, "w", encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    # Convert JSON to markdown and save it
    md_filename = f"{base_path+relative_path}"
    md_data = json2md(json_data) + "\n\n# 𝍖user\n"
    with open(md_filename, "w", encoding='utf-8') as md_file:
        md_file.write(md_data)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage incorrect")
    else:
        main(sys.argv[1],sys.argv[2])
