from . import utils


"""
Generate the file path for uploading user files.

The uploaded file will be stored in the following format:
    MEDIA_ROOT/user_<id>/<type>/<unique_id>.<extension>

Parameters:
    instance: An instance of the model representing the user.
    filename (str): The original filename of the uploaded file.

Returns:
    str: The formatted file path for storing the uploaded file.
"""


def user_profile_path(instance, filename):
    '''
    Path to store user's profile images: <instance.id>/profiles/<filename>
    '''

    extension = filename.split('.')[-1]
    new_file_name = f'{utils.generate_random_ids}.{extension}'

    return f'{instance.id}/profile/{new_file_name}'


def user_documents_path(instance, filename):
    '''
    Path to store user's documaents: <instance.id>/documents/<filename>
    '''

    extension = filename.split('.')[-1]
    new_file_name = f'{utils.generate_random_ids}.{extension}'

    return f'{instance.id}/documents/{new_file_name}'


def application_uploads(instance, filename):
    '''
    Path to store user's application: jobs/<job_created_date>/<instance.id>/<filename>
    '''

    extension = filename.split('.')[-1]
    new_file_name = f'{utils.generate_random_ids}.{extension}'

    return f'jobs/{str(instance.job_id.created_at.date())}/{instance.user_id.id}/{new_file_name}'
