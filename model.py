import psycopg2

def dconn():
    conn = psycopg2.connect(database='project_f0bg', host='dpg-ci488ldiuie031gv8mf0-a.oregon-postgres.render.com', user='intaylor', password='9X6letKDo4gJPwxIDGECmHoRhFht7sgG', port=5432)
    return conn


def get_password(username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    data = cur.fetchall()
    password = data[0][2]
    cur.close()
    conn.close()
    return password


def update_email(email, username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("UPDATE Users SET email=%s WHERE username=%s", (email, username,))
    conn.commit()
    cur.close()
    conn.close()


def update_password(password, username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("UPDATE Users SET password=%s WHERE username=%s", (password, username,))
    conn.commit()
    cur.close()
    conn.close()


def save_user(username, email, password):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO Users(username, email, password) VALUES(%s, %s, %s)", (username, email, password,))
    conn.commit()
    cur.close()
    conn.close()


def post_image(image_name, serialized_image, pred, username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO Post(image_name, image_data, prediction, username) VALUES(%s, %s, %s, %s)", (image_name, psycopg2.Binary(serialized_image), pred, username,))
    conn.commit()
    cur.close()
    conn.close()


def get_username_count(username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Users WHERE username=%s", (username,))
    data = cur.fetchall()
    username_count = data[0][0]
    cur.close()
    conn.close()
    return username_count


def get_details(username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE username=%s", (username,))
    data = cur.fetchall()
    dic = {
        'username': data[0][0],
        'email': data[0][1],
    }
    cur.close()
    conn.close()
    return dic


def get_post_count(username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Post WHERE username=%s", (username,))
    data = cur.fetchall()
    post_count = data[0][0]
    cur.close()
    conn.close()
    return int(post_count)


def get_images_data(username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Post WHERE username=%s", (username,))
    data = cur.fetchall()
    images_data = []
    for i in data:
        images_data.append({
            'image_name': i[2],
            'image_data': i[3],
            'prediction': i[4]
        })
    cur.close()
    conn.close()
    return images_data

def get_last_post(username):
    conn = dconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Post WHERE username=%s ORDER BY id DESC LIMIT 1", (username,))
    data = cur.fetchall()
    data = data[0]
    dic = [{
        'image_name': data[2],
        'image_data': data[3],
        'prediction': data[4]
    }]
    cur.close()
    conn.close()
    return dic