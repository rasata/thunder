import json


def topng(images, path, prefix="image", overwrite=False, credentials=None):
    """
    Write out PNG files for 2d or 3d image data.

    See also
    --------
    thunder.data.images.topng
    """
    dims = images.dims
    if not len(dims) in [2, 3]:
        raise ValueError("Only 2D or 3D images can be exported to png, "
                         "images are %d-dimensional." % len(dims))

    from scipy.misc import imsave
    from io import BytesIO
    from thunder.data.writers import get_parallel_writer

    def tobuffer(kv):
        key, img = kv
        fname = prefix+"-"+"%05d.png" % int(key)
        bytebuf = BytesIO()
        imsave(bytebuf, img, format='PNG')
        return fname, bytebuf.getvalue()

    writer = get_parallel_writer(path)(path, overwrite=overwrite, credentials=credentials)
    images.foreach(lambda x: writer.write(tobuffer(x)))

def totif(images, path, prefix="image", overwrite=False, credentials=None):
    """
    Write out TIF files for 2d or 3d image data.

    See also
    --------
    thunder.data.images.totif
    """
    dims = images.dims
    if not len(dims) in [2, 3]:
        raise ValueError("Only 2D or 3D images can be exported to tif, "
                         "images are %d-dimensional." % len(dims))

    from scipy.misc import imsave
    from io import BytesIO
    from thunder.data.writers import get_parallel_writer

    def tobuffer(kv):
        key, img = kv
        fname = prefix+"-"+"%05d.tif" % int(key)
        bytebuf = BytesIO()
        imsave(bytebuf, img, format='TIFF')
        return fname, bytebuf.getvalue()

    writer = get_parallel_writer(path)(path, overwrite=overwrite, credentials=credentials)
    images.foreach(lambda x: writer.write(tobuffer(x)))

def tobinary(images, path, prefix="image", overwrite=False, credentials=None):
    """
    Write out binary files for image data.

    See also
    --------
    thunder.data.images.tobinary
    """
    from thunder.data.writers import get_parallel_writer

    dims = list(images.dims)

    def tobuffer(kv):
        key, img = kv
        fname = prefix + "-" + "%05d.bin" % int(key)
        return fname, img.copy()

    writer = get_parallel_writer(path)(path, overwrite=overwrite, credentials=credentials)
    images.foreach(lambda x: writer.write(tobuffer(x)))
    config(path, dims=dims, dtype=images.dtype, overwrite=overwrite)

def config(path, dims, dtype='int16', name="conf.json", overwrite=True, credentials=None):
    """
    Helper function to write a JSON file with configuration for binary image data.
    """
    from thunder.data.writers import get_file_writer

    writer = get_file_writer(path)

    conf = {'dims': dims, 'dtype': str(dtype)}
    confwriter = writer(path, name, overwrite=overwrite, credentials=credentials)
    confwriter.write(json.dumps(conf, indent=2))

    successwriter = writer(path, "SUCCESS", overwrite=overwrite, credentials=credentials)
    successwriter.write('')