from module import my_module

if __name__ == "__main__":
    celsius = float(input("Enter a temperature in Celsius: "))
    fahrenheit = my_module.c_to_f(celsius)
    print("That's %f degree Fahrenheit" % fahrenheit)
