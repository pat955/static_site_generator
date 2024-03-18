import re
from textnode import TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    del_count = len(delimiter)
    for node in old_nodes:
        if type(node) != TextNode or node.text_type != "text":
            new_nodes.append(node)
            continue
       
        split_nodes = re.split(f"[{delimiter}]{{{del_count}}}(.*?)[{delimiter}]{{{del_count}}}", node.text)
        
        matches = re.findall(f"[{delimiter}]{{{del_count}}}(.*?)[{delimiter}]{{{del_count}}}", node.text)
        
        for text in split_nodes:
            if text in matches:
                new_nodes.append(TextNode(text, text_type))
                continue
            new_nodes.append(TextNode(text, "text"))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^ ]*?)\]\(([^ ]*?)\)", text)

def extract_markdown_links(text):
    i = 0 
    links = []
    split_text = re.split(r"(\[[^ ]*?\]\([^ ]*?\))", text)
    for t in split_text:
        if i == 0:
            i += 1
            continue

        if split_text[i-1][-1] != '!' and re.match(r"\[([^ ]*?)\]\(([^ ]*?)\)", t):
            links.append(t)
        i += 1
    return re.findall(r"\[([^ ]*?)\]\(([^ ]*?)\)", ''.join(links))


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        temp_merged_str = ""
        
        if node.text == None:
            continue

        images = extract_markdown_images(node.text)
        
        if not images:
            new_nodes.append(node)
            continue
        
        split = re.split(r"(!\[[^ ]*?\]\([^ ]*?\))", node.text)

        for new_node in split:
            if new_node == "":
                continue

            try:
                image_tuple = re.findall(r"!\[([^ ]*?)\]\(([^ ]*?)\)", new_node)[0]
                
            except Exception as e:
                image_tuple = []

            if image_tuple in images:
                if temp_merged_str != "":
                    new_nodes.append(TextNode(temp_merged_str, "text"))
                    temp_merged_str = ""

                new_nodes.append(TextNode(image_tuple[0], "image", image_tuple[1]))
        
            else:
                temp_merged_str += new_node

        if temp_merged_str != "":
            new_nodes.append(TextNode(temp_merged_str, "text"))
    
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        temp_merged_str = ""
        if node.text == None:
            continue

        links = extract_markdown_links(node.text)
        
        if not links:
            new_nodes.append(node)
            continue
        
        split =  re.split(r"(\[[^ ]*?\]\([^ ]*?\))", node.text)
        
        for new_node in split:
            if new_node == "":
                continue
            
            try:
                link_tuple = re.findall(r"\[([^ ]*?)\]\(([^ ]*?)\)", new_node)[0]
                
            except Exception as e:
                link_tuple = []

            if link_tuple in links:
                if temp_merged_str != "":
                    new_nodes.append(TextNode(temp_merged_str, "text"))
                    temp_merged_str = ""

                new_nodes.append(TextNode(link_tuple[0], "link", link_tuple[1]))
            else:
                temp_merged_str += new_node

        if temp_merged_str != "":
            new_nodes.append(TextNode(temp_merged_str, "text"))
    return new_nodes