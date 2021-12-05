from importlib import import_module

def get_face_transformation_matrix(old_landmarks, new_landmarks):
    np = import_module('numpy')
    bias = np.ones((len(old_landmarks),))
    D = np.array(old_landmarks)

    D = np.insert(D, 3, 1, axis= 1)
    Y = np.array(new_landmarks)
    Y = np.insert(Y, 3, 1, axis= 1)

    # w = (D.T D)^-1 D.T Y
    w = np.linalg.inv(D.T.dot(D)).dot(D.T).dot(Y)
    w[np.abs(w) < 0.000001] = 0
    return w