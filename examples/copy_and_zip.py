from rdp_manipulations import RDP
from datetime import date

connection = RDP(headless=False, width=800, height=600)
connection.login(guacamole_url='http://localhost:8080/guacamole/#/', guacamole_user='guacadmin',
                 guacamole_password='guacadmin', guacamole_pc_name='win7en')

connection.mkdir('C:\\foo')
connection.exec_remote('net use U: \\\\tsclient\\U')  # NOTE: connect network drive provided by guacamole
connection.copy('U:\\bar', 'C:\\foo\\')
connection.opendir('C:\\foo')

connection.key_press("Control+KeyA")
connection.key_press("ContextMenu")

if connection.mouse_move_to('./examples/asserts/send_to.png') and connection.mouse_click_to('./examples/asserts/zip.png'):
    today_date = str(date.today())
    connection.key_type(f'{today_date}.zip')
    connection.make_screenshot(path='./examples/copy_and_zip_done.png')
