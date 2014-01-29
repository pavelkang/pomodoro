def detag(s):
    start = s.find("<en-note>")
    string = s[start:]
    #num = 2*(string.count("</")) + string.count("/>")
    num = string.count("<")
    for i in xrange(num):
        start = string.find("<")
        end = string.find(">")
        if string[start:end+1] != "<div>":
            string = string[:start] + string[end+1:]
        else:
            string = string[:start] + "{}" + string[end+1:]
    l = string.split("{}")
    tasks = []
    for i in l:
        if i != '':
            tasks.append(i)
    return tasks
