from io import BytesIO
import fastavro

from fastavro.read import _read as _reader
from fastavro.write import _write as _writer, Writer


schema = {"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}

def serialize(schema, data):
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, data)
    return bytes_writer.getvalue()

def deserialize(schema, binary):
    bytes_writer = BytesIO()
    bytes_writer.write(binary)
    bytes_writer.seek(0)
    data = fastavro.schemaless_reader(bytes_writer, schema)
    return data

avro_test_ser = serialize(schema, {"name": '123', "favorite_number": 321, 'favorite_color': 'red' })
avro_test_deser = deserialize(schema, avro_test_ser)