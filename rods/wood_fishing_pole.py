def getMask(hsvFrame, np, cv2):
    # create brown mask
    brown_lower = np.array([10, 0, 0], np.uint8)
    brown_upper = np.array([20, 255, 255], np.uint8)
    brown_mask = cv2.inRange(hsvFrame, brown_lower, brown_upper)

    return brown_mask