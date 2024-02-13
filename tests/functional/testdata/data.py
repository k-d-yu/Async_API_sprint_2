from pydantic import BaseModel


class TestData(BaseModel):

    incorrect_id: str = '0a0a0aa0-0a00-0000-00aa-0aaa0a0a00aa'
    genre_id: str = '39d312c0-5357-4dd1-bddb-d732a85a6618'
    person_id: str = '156c0a4d-4985-4fc3-a012-372fcb0bc902'
    movie_id: str = '5af006c4-09d4-4ccc-a62e-04f38bd1dce4'
    genre_title: str = 'expedit'


test_data = TestData()
