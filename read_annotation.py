import scipy.io

image_path = 'data/PA-100K/data/'
annotation_path = 'data/PA-100K/annotation.mat'

mat = scipy.io.loadmat(annotation_path)
print(mat.keys())

train_images = mat['train_images_name']
train_label = mat['train_label']
# print(mat['attributes'])


# for i in range(5):
#     print(f"Image: {train_images[i][0]}")
#     print(f"Attributes: {train_label[i]}")


class PedestrianSample:
    """
    統一行人屬性分析資料結構
    image_path: 影像檔案路徑
    bbox: [x1, y1, x2, y2]，如有 bounding box 資訊可填入，否則可為 None
    attributes: 屬性標籤 list（0/1），依照 PA-100K 的 attributes 順序
    """
    def __init__(self, image_path, bbox, attributes):
        self.image_path = image_path
        self.bbox = bbox
        self.attributes = attributes
    def __repr__(self):
        return f"PedestrianSample({self.image_path}, {self.bbox}, {self.attributes})"
    
sample = PedestrianSample(image_path + train_images[0][0], None, train_label[0].tolist())
print(sample)