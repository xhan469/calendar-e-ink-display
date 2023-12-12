from flask import Flask, request, render_template_string, jsonify, redirect, url_for, session
import gkeepapi
import os
import socket


import os




def get_ip_address():
    try:
        # Attempt to connect to an external IP to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error obtaining IP address: {e}")
        return None

# Initialize Flask app
secret_key = os.urandom(16)
app = Flask(__name__)
app.secret_key = secret_key

# Initialize the GPIO

def write_wifi_config(ssid, password):
    if not ssid or not password:
        print("SSID or password cannot be empty.")
        return False

    existing_networks = {}
    try:
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as f:
            lines = f.readlines()

        in_network_block = False
        current_ssid = None
        for line in lines:
            line = line.strip()
            if "network={" in line:
                in_network_block = True
            elif "}" in line:
                in_network_block = False
                current_ssid = None
            elif in_network_block:
                if "ssid=" in line:
                    current_ssid = line.split("=")[1].strip('"')
                elif "psk=" in line and current_ssid:
                    existing_networks[current_ssid] = line.split("=")[1].strip('"')

        existing_networks[ssid] = password

        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
            f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
            f.write("update_config=1\n")
            for ssid, psk in existing_networks.items():
                if ssid == "calendar":
                    f.write("network={\n")
                    f.write(f'    ssid="calendar"\n')
                    f.write(f'    psk="calendar"\n')
                    f.write(f'    priority=1\n')
                    f.write("}\n")
                else:
                    f.write("network={\n")
                    f.write(f'    ssid="{ssid}"\n')
                    f.write(f'    psk="{psk}"\n')
                    f.write("}\n")

        print(f"Written SSID: {ssid}, Password: {password}")
        return True

    except PermissionError:
        print("Permission denied: Run this script as root to modify wpa_supplicant.conf")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



@app.route('/', methods=['GET', 'POST'])
def index():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mode_file_path = os.path.join(script_dir, "setting/mode.txt")
    pass_file_path = os.path.join(script_dir, "setting/password.txt")
    brightness_file_path = os.path.join(script_dir, "setting/brightness.txt")

    message = ''
    check_account = ''
    account_info = ''
    account_pass = ''
    account_list = ''
    delete_button = '   <button type="button" class="delete-button" data-account="' + account_info + '" style="background-color: black; color: white; padding: 5px 10px; border: none; cursor: pointer;">Delete</button>'

    mode = ''
    brightness = 0.1

    try:
        with open(brightness_file_path, "r") as f:
            lines = f.readlines()
            if len(lines) == 1:
                brightness = lines[0]
    except FileNotFoundError:
        print("mode.txt not found")

    try:
        with open(mode_file_path, "r") as f:
            lines = f.readlines()
            if len(lines) == 1:
                mode = lines[0]
    except FileNotFoundError:
        print("mode.txt not found")


    # Read the account info when the page loads
    try:
        with open(pass_file_path, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                account_info = lines[i].strip()
                account_pass = lines[i+1].strip()

                try:
                    keep = gkeepapi.Keep()
                    success = keep.login(account_info, account_pass)

                    if success:
                        account_list += account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '">Delete</button>' +'<br><br>'
                        if check_account == '':
                            check_account = ' (valid login)' + '<br><br>'

                    else:
                        check_account = '<span style="color: red;">' + ' Bad Authentication, please check network status or see following link for more information about the 2 way Auth: <a href="https://support.google.com/accounts/answer/185833?hl=en" target="_blank">here</a></span>' + '<br><br>'
                        account_list += '<span style="color: red;">' + account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '">Delete</button>' + '</span><br><br>'
                except gkeepapi.exception.LoginException:
                    account_list += '<span style="color: red;">' + account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '">Delete</button>' + '</span><br><br>'
                    check_account = '<span style="color: red;">'  + ' Bad Authentication, please check network status or see following link for more information about the 2 way Auth: <a href="https://support.google.com/accounts/answer/185833?hl=en" target="_blank">here</a></span>' + '<br><br>'
                except Exception as e:
                    account_list += '<span style="color: red;">' + account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '">Delete</button>' + '</span><br><br>'
                    check_account = '<span style="color: red;">'  + ' Bad Authentication, please check network status or see following link for more information about the 2 way Auth: <a href="https://support.google.com/accounts/answer/185833?hl=en" target="_blank">here</a></span>' + '<br><br>'


    except FileNotFoundError:
        print("password.txt not found")
    except Exception as e:
        print(f"An error occurred while reading password.txt: {e}")


    if request.method == 'POST':
        brightness = request.form['brightnessValue']

        if mode:
            f = open(brightness_file_path, "w")
            f.write(brightness)
            f.close()

        if mode:
            f = open(mode_file_path, "w")
            f.write(mode)
            f.close()

        ssid = request.form['wifi_ssid']
        password = request.form['wifi_pass']

        account = request.form['google_ssid']
        account_pass = request.form['google_pass']
        print(account, account_pass)

        mode = 'light' if 'dark_light_mode' in request.form else 'dark'
        print("going to write", mode)

        if mode:
            f = open(mode_file_path, "w")
            f.write(mode)
            f.close()

        if account and account_pass:
            account_info = account
            updated = False

            try:
                with open(pass_file_path, 'r') as file:
                    lines = file.readlines()
            except FileNotFoundError:
            # Create the file and set lines to empty
                open(pass_file_path, 'w').close()
                with open(pass_file_path, 'r') as file:
                    lines = file.readlines()

            with open(pass_file_path, 'w') as file:
                for i in range(0, len(lines), 2):  # Step through two lines at a time (account and password)
                    if lines[i].strip() == account_info:
                        # Update the password
                        lines[i + 1] = account_pass + "\n"
                        updated = True
                    file.write(lines[i])
                    if i + 1 < len(lines):
                        file.write(lines[i + 1])

            if not updated:
                # Append new account and password
                with open(pass_file_path, 'a') as file:
                    file.write(account_info + "\n" + account_pass + "\n")

            message = "Account information and password updated successfully!"

            try:
                keep = gkeepapi.Keep()
                success = keep.login(account_info, account_pass)

                if success:
                    account_list += account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '">Delete</button>' + '<br><br>'
                    if check_account == '':
                        check_account =' (valid login)' + '<br><br>'

                else:
                    account_list += '<span style="color: red;">' + account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '" style="background-color: black; color: white; padding: 5px 10px; border: none; cursor: pointer;">Delete</button>' + '</span><br><br>'
                    check_account = '<span style="color: red;">' + ' Bad Authentication, please check network status or see following link for more information about the 2 way Auth: <a href="https://support.google.com/accounts/answer/185833?hl=en" target="_blank">here</a></span>' + '<br><br>'
            except gkeepapi.exception.LoginException:
                account_list += '<span style="color: red;">' + account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '" style="background-color: black; color: white; padding: 5px 10px; border: none; cursor: pointer;">Delete</button>' + '</span><br><br>'
                check_account = '<span style="color: red;">' + ' Bad Authentication, please check network status or see following link for more information about the 2 way Auth: <a href="https://support.google.com/accounts/answer/185833?hl=en" target="_blank">here</a></span>' + '<br><br>'
            except Exception as e:
                account_list += '<span style="color: red;">' + account_info + '   <button type="button" class="delete-button" data-account="' + account_info + '" style="background-color: black; color: white; padding: 5px 10px; border: none; cursor: pointer;">Delete</button>' + '</span><br><br>'
                check_account = '<span style="color: red;">' + ' Bad Authentication, please check network status or see following link for more information about the 2 way Auth: <a href="https://support.google.com/accounts/answer/185833?hl=en" target="_blank">here</a></span>' + '<br><br>'
        #print('test')



        if ssid and password:
            # Write to wifi config
            if write_wifi_config(ssid, password):
                message += "Written to WiFi config successfully!"
            else:
                message += "Failed to write to WiFi config!"
        else:
            message += "\ngoogle account information hasn't updated yet, please fill both wifi name and password to update"


        # Serve the HTML form
        script_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(script_dir, 'templates/index.html')

        with open(index_path, 'r') as f:
            form_content = f.read()

        session['message'] = message
        session['account'] = account_info
        session['check_account'] = check_account
        session['mode'] = mode
        session['brightness'] = brightness
        session['account_list'] = account_list

        return redirect(url_for('index'))

    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, 'templates/index.html')

    with open(index_path, 'r') as f:
        form_content = f.read()

    '''
    session['message'] = message
    session['account'] = account_info
    session['check_account'] = check_account
    session['mode'] = mode
    session['brightness'] = brightness
    session['account_list'] = account_list'''

    return render_template_string(form_content, message = message, account = account_info, check_account = check_account, mode = mode, brightness = brightness, account_list = account_list)
    #return render_template_string(form_content)


@app.route('/delete_account', methods=['POST'])
def delete_account():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pass_file_path = os.path.join(script_dir, "setting/password.txt")

    data = request.json
    account_to_delete = data['account']


    with open(pass_file_path, 'r') as file:
        lines = file.readlines()

    with open(pass_file_path, 'w') as file:
        skip_next = False
        for line in lines:
            if skip_next:
                skip_next = False
                continue
            if line.strip() == account_to_delete:
                skip_next = True
                continue
            file.write(line)


    return jsonify({"message": "Account deleted successfully"})



if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Connect to a remote server (Google's public DNS server)
    s.connect(("8.8.8.8", 80))

    # Get the local IP address of the machine
    local_ip = s.getsockname()[0]

    # Close the socket
    s.close()

    ip_address = get_ip_address()
    if ip_address:
        app.run(host=local_ip, port=5000, debug=True)
    else:
        print("Could not determine the IP address. Flask application not started.")

