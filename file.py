try:
    f1 = open('/home/will/桌面/Python/questionnaire/properties/part1.txt')
    f2 = open('/home/will/桌面/Python/questionnaire/properties/part2.txt')
    f3 = open('/home/will/桌面/Python/questionnaire/properties/part3.txt')
except IOError as identifier:
    pass
finally:
    f1.close()
    f2.close()
    f3.close()

print(f1.read())
print(f2.read())
print(f3.read())