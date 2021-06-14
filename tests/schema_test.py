from database.db import dbsession
from database.schema import Users, Files


# with dbsession() as session:
    # session.add(user)
    # session.commit()
    # file1 = Files(file_name="1.txt", file_path="1.txt", date_added=datetime(1999,5,21).date())
    # file2 = Files(file_name="2.txt", file_path="2.txt", date_added="1999-06-29")
    # session.add_all([file1])
    # session.commit()
    # result = session.query(Files).filter(Files.file_name=="1.txt").all()
    # list_of_files = list(result)
    # user = Users(user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", name="Tushar Singh", password="1999", username="tusharvickey1999")
    # user2 = Users(user_id="3fa85f64-5717-4562-b3fc-2c963f66afa7", name="string", password="string", username="string")
    # user.file = list_of_files
    # session.add_all([user, user2])
    # session.commit()
    # for row in result:
    #     print(row.user_id)
    # print(user)
    # print(user2)
