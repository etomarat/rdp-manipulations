from rdp_manipulations import RDP

connection = RDP(headless=False, width=800, height=600)
connection.login(guacamole_url='http://localhost:8080/guacamole/#/', guacamole_user='guacadmin', guacamole_password='guacadmin', guacamole_pc_name='win7en')
while (True):
    screenshot_name = input('Enter screenshot name:')
    connection.make_screenshot(screenshot_name)
    # connection.make_screenshot(path=f'{screenshot_name}.png')
