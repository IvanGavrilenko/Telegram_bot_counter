from ultralytics import YOLO
#model_n = YOLO("yolo11n.pt")
#results_n = model_n.train(data="E:\\python\\Rolls.v5i.yolov11\\data.yaml", epochs=100, imgsz=640)

#model_s = YOLO("yolo11s.pt")
#results_s = model_s.train(data="E:\\python\\Rolls.v5i.yolov11\\data.yaml", epochs=100, imgsz=640)

model_m = YOLO("yolo11m.pt")
results_m = model_m.train(data="E:\\python\\Rolls.v5i.yolov11\\data.yaml", epochs=100, imgsz=640)

model_l = YOLO("yolo11l.pt")
results_l = model_l.train(data="E:\\python\\Rolls.v5i.yolov11\\data.yaml", epochs=100, imgsz=640)

model_x = YOLO("yolo11x.pt")
results_x = model_x.train(data="E:\\python\\Rolls.v5i.yolov11\\data.yaml", epochs=100, imgsz=640)
