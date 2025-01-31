def float_entry(val, min_limit, max_limit):
    #For setting the string values back to float
    min_limit = float(min_limit)
    max_limit = float(max_limit)

    # Validation if entry is empty
    if val == "":
        return True

    #Validation if negative numbers are allowed:
    if val == "-" and min_limit < 0:
        return True

    #Could add a validation for starting with "." and just add a 0 at the start, todo later

    #Disallow multiple zeroes
    if val[0] == "0" and len(val) > 1 and val[1] != ".":
        return False

    allow_temp = False #Declaration of boolean
    if ("." in str(min_limit)) or (len(str(abs(int(min_limit)))) > 2): #Checking if decimal, and if multiple numbers are required
        allow_temp = True #Allow temporary values for proper entries

    #Allows for only up to 2 decimal places
    if "." in val and len(val.split(".")[-1]) > 2:
        return False

    # Validation if the user has entered an actual integer
    try:
        value = float(val)
    except ValueError:
        return False

    if not allow_temp: #Check if it passes the vibe
        if min_limit <= value <= max_limit:
            return True
        else:
            return False

    #Everything after here is checked only if temp values are allowed
    if val == str(min_limit)[0]:
        return True

    # Check if it's the first value inputted and if it is inbetween the min and max value
    # Only works if both values are positive and are greater than 0, for values both negative, the system fails
    power = len(str(abs(int(min_limit))))
    minn = min_limit // (10**power)
    maxx = max_limit // (10**power)
    if len(val.replace("-", "")) == 1 and minn < value < maxx:
        return True

    # Check if whole value is still temp value
    if len(val.split(".")[0]) < len((str(abs(min_limit))).split(".")[0]):
        return True

    #Checks if entry is a decimal
    if "." in val:
        # Check if decimal value is still temp value
        if len(val.split(".")[1]) < len((str(abs(min_limit))).split(".")[1]):
            return True

    # Finally can perform vibe check
    if min_limit <= value <= max_limit:
        return True

    #Invalidate if conditions are not passed
    return False

