import jinja2 


loader=jinja2.FileSystemLoader("deployment_files")
env=jinja2.Environment(loader=loader)
template = loader.load(env, ".env.j2")
secret_key = input("Enter secret key (for cookie encryption): ")
trello_token = input("Enter trello token: ")
trello_board = input("Enter trello board id: ")
rendered = template.render(secret_key=secret_key, trello_token=trello_token, trello_board=trello_board)
with open("deployment_files/.env", "w") as file:
    file.write(rendered)