import winreg
import time
import datetime

def log_message(message, force_log=False):
    # Show logs only if force_log is True
    if force_log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

def check_and_delete_bseed():
    try:
        # Open the registry key
        key_path = r"Honeycomb2"
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
        
        try:
            # Check if the bseed value exists
            value, reg_type = winreg.QueryValueEx(key, "bseed")
            
            # If we get here, the value exists
            # Verify that it's a DWORD (type 4)
            if reg_type == winreg.REG_DWORD:
                # Delete the bseed value
                winreg.DeleteValue(key, "bseed")
                winreg.CloseKey(key)
                return True
            else:
                winreg.CloseKey(key)
                return False
                
        except FileNotFoundError:
            # The value doesn't exist
            winreg.CloseKey(key)
            return False
            
    except FileNotFoundError:
        # The key doesn't exist
        return False
    except Exception as e:
        # Handle other exceptions
        return False

def main():
    count = 1
    
    while True:
        result = check_and_delete_bseed()
        
        if result:
            log_message(f"Iteration #{count}: bseed found and deleted", True)
            log_message("Operation details: Registry key HKEY_CLASSES_ROOT\\Honeycomb2 processed successfully", True)
            count += 1

if __name__ == "__main__":
    main()