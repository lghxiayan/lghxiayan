class MyClass:
    class_attribute = "这是一个类属性"

    def method1(self):
        print("-" * 30)
        print(MyClass.class_attribute)  # 访问类属性
        print(self.class_attribute)  # 也可以通过实例访问类属性
        print("-" * 30)

    def method2(self):
        self.instance_attribute = "这是一个实例属性"  # 创建实例属性
        print(self.instance_attribute)


# 使用类属性
obj = MyClass()
obj.method1()  # 输出: 这是一个类属性
obj.method2()  # 输出: 这是一个实例属性

# 类属性可以被所有实例共享
obj2 = MyClass()
print(obj2.class_attribute)  # 输出: 这是一个类属性
obj2.class_attribute = '222'
print(obj2.class_attribute)

print(obj.class_attribute)
