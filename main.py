### 
import glob
import psycopg2
import os
import time
from dotenv import load_dotenv

#Carregando variaveis
load_dotenv()

db_name = os.getenv('DB_NAME')
db_password = os.getenv('DB_PASSWORD')


while True:
    try:
        env_files = glob.glob('/home/botcrm/*/backend/.env')
        env_file_path = env_files[0]

        with open(env_file_path, 'r') as file:
            for line in file:
                if 'DB_NAME=' in line:
                    namechat_value = line.split('=')[1].strip()
                    print(namechat_value)
                    print(db_name)
                    print(db_password)
                    break

            else:
                print('Linha NAME_CHAT não encontrado')

        conn = psycopg2.connect(
            dbname = f"{namechat_value}",
            user = f"{db_name}",
            password = f"{db_password}",
            host = "172.17.0.1"
        )

        cur = conn.cursor()

        cur.execute("""

                select id from "Tickets" t where t."queueId" is null 

                    """)
        
        rows = cur.fetchall()
        print(rows)

        if len(rows) >= 1:
            print('Existe ticket sem fila')

            for row in rows:
                ticket_id = row[0]

                cur.execute(f"""

                    update "Tickets" 
                    set "queueId" = 1
                    where id = {ticket_id}

                            """)
                

                print(f"O ticket {ticket_id} foi transferido para a fila")
                conn.commit()
    
            cur.close()
            conn.close()

    except psycopg2.Error as e:
        print("Erro ao conectar no banco de dados")
        print(e)

    time.sleep(1 * 60)
