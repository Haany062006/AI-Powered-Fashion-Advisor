from backend.services.body_shape import detect_body_shape

result = detect_body_shape("uploads/test.jpg")
print(result)