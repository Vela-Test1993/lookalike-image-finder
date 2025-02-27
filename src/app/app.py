import homepage

search_option = ['Select an option','Search by text', 'Search by image']

homepage.setup_page()

choosen_option = homepage.get_user_selection(search_option)
if choosen_option.lower() == 'search by text':
    user_query = homepage.get_search_text_input()
    if user_query:
        homepage.get_images_by_text(user_query)
elif choosen_option.lower() == 'search by image':
    image_input = homepage.get_search_image_input()
    if image_input:
        homepage.get_images_by_image(image_input)

