from rdp_manipulations.main import RDP

connection = RDP(headless=False, width=800, height=600)
connection.login(guacamole_url='http://localhost:8080/guacamole/#/', guacamole_user='guacadmin', guacamole_password='guacadmin', guacamole_pc_name='win7en')
connection.mkdir('C:\\foo')
connection.exec_remote('net use U: \\\\tsclient\\U')  # NOTE: connect network drive provided by guacamole
connection.copy('U:\\bar', 'C:\\foo\\')
connection.opendir('C:\\foo')
connection.key_press("Control+KeyA")
connection.key_press("ContextMenu")
while (True):
    screenshot_name = input('Enter screenshot name:')
    connection.make_screenshot(screenshot_name)
    # connection.make_screenshot(path=f'{screenshot_name}.png')
