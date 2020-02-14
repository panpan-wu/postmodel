
from postmodel import Postmodel, models
import pytest
from postmodel.exceptions import (
    IntegrityError,
    OperationalError,
    DoesNotExist,
    MultipleObjectsReturned)
import asyncio
from postmodel.models import QueryExpression, Q
from postmodel.models import functions as fn
from tests.testmodels import (Foo, Book,
    CharFieldsModel)

@pytest.mark.asyncio
async def test_api_1(db_url):
    await Postmodel.init(db_url, modules=[__name__])
    assert len(Postmodel._databases) == 1
    assert Postmodel._inited == True
    await Postmodel.generate_schemas()
    
    await CharFieldsModel.all().delete()

    m = await CharFieldsModel.create(id=1, char="hello", char_null="hi")
    await CharFieldsModel.bulk_create([
        CharFieldsModel(id=2, char="hello2"),
        CharFieldsModel(id=3, char="hello3", char_null="null3"),
        CharFieldsModel(id=4, char="hello4", char_null="null4"),
        CharFieldsModel(id=5, char="hello5")
    ])
    
    mlist = await CharFieldsModel.exclude(id = 3)
    assert len(mlist) == 4

    mlist = await CharFieldsModel.filter(id__in = [2, 4])
    assert len(mlist) == 2
    mlist = await CharFieldsModel.exclude(id__not_in = [2, 4])
    assert len(mlist) == 2

    mlist = await CharFieldsModel.exclude(id__in = [2, 4])
    assert len(mlist) == 3

    mlist = await CharFieldsModel.filter(id__not_in = [2, 4])
    assert len(mlist) == 3

    ret = await CharFieldsModel.get_or_none(id = 14)
    assert ret == None

    ret = await CharFieldsModel.all().get_or_none(id=42)
    assert ret == None

    ret = await CharFieldsModel.filter(Q(id__in=[3])).first()
    assert ret.id == 3

    ret = await CharFieldsModel.exclude(Q(id__in=[1,2,3,4])).first()
    assert ret.id == 5

    async for cfm in CharFieldsModel.filter(id__in = [2, 4]):
        assert cfm.id in [2, 4]

    obj, created = await CharFieldsModel.get_or_create(
            id = 5,
            defaults={'char_null': "get_or_create"}
        )
    assert created == False
    assert obj.id == 5
    assert obj.char_null == None

    obj, created = await CharFieldsModel.get_or_create(
            id = 5
        )
    assert created == False
    assert obj.id == 5

    obj, created = await CharFieldsModel.get_or_create(
            id = 25,
            defaults={'char':"get_or_create", 'char_null': "get_or_create_null"}
        )
    assert created == True
    assert obj.id == 25
    assert obj.char == "get_or_create"

    await CharFieldsModel.all().delete()
    await Postmodel.close()


@pytest.mark.asyncio
async def test_api_queries(db_url):
    await Postmodel.init(db_url, modules=[__name__])
    assert len(Postmodel._databases) == 1
    assert Postmodel._inited == True
    await Postmodel.generate_schemas()
    
    await CharFieldsModel.bulk_create([
        CharFieldsModel(id=2, char="Hello Moo World"),
        CharFieldsModel(id=3, char="HELLO WWW", char_null="null3"),
        CharFieldsModel(id=4, char="postMODEL works", char_null="null4"),
        CharFieldsModel(id=5, char="aSyNCio rocks"),
        CharFieldsModel(id=6, char="Hello MOO World"),
    ])
    async for obj in CharFieldsModel.filter(char__contains="or"):
        assert "or" in obj.char
    
    mlist  = await CharFieldsModel.filter(char__icontains="hello")
    assert len(mlist) == 3
    for obj in mlist:
        assert "hello" in obj.char.lower()
    
    async for obj in CharFieldsModel.filter(char__startswith="He"):
        assert obj.char.startswith("He")
    
    async for obj in CharFieldsModel.filter(char__istartswith="He"):
        assert obj.char[0:2].lower() == "he"
    
    async for obj in CharFieldsModel.filter(char__endswith="ks"):
        assert obj.char.endswith("ks")
    
    async for obj in CharFieldsModel.filter(char__iendswith="KS"):
        assert obj.char[-2:].upper() == "KS"
    
    async for obj in CharFieldsModel.filter(char__iexact="Hello Moo World"):
        assert obj.char.upper() == "HELLO MOO WORLD"

    async for obj in CharFieldsModel.filter(id__not=3):
        assert obj.id != 3

    async for obj in CharFieldsModel.filter(id__gt=3):
        assert obj.id > 3

    async for obj in CharFieldsModel.filter(id__gte=3):
        assert obj.id >= 3

    async for obj in CharFieldsModel.filter(id__lt=3):
        assert obj.id < 3

    async for obj in CharFieldsModel.filter(id__lte=3):
        assert obj.id <= 3

    async for obj in CharFieldsModel.filter(char_null__isnull=True):
        assert obj.char_null == None
    
    async for obj in CharFieldsModel.filter(char_null__isnull=False):
        assert obj.char_null != None
    
    async for obj in CharFieldsModel.filter(char_null__not_isnull=True):
        assert obj.char_null != None

    async for obj in CharFieldsModel.filter(char_null__not_isnull=False):
        assert obj.char_null == None

    await CharFieldsModel.all().delete()

    await Postmodel.close()