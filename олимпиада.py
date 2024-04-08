def human_read_format(size):
    count = 1
    b = ['КБ', 'МБ', 'ГБ']
    if size < 1024:
        return str(size) + 'Б'
    else:
        a = size / 1024
        for i in range(3):
            if a > 1024:
                a = round(a / 1024)
                print(a)
                count += 1
                print(count)
        return str(a) + b[count - 1]


print(human_read_format(15000))