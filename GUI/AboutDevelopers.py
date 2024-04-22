# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk
# import webbrowser

# def aboutDevelopers_page():
#     try:
#         def open_url(url):
#             webbrowser.open_new_tab(url)

#         def go_back():
#             aboutdev_win.destroy()

#         aboutdev_win = tk.Tk()
#         aboutdev_win.title('About The Developers')
#         aboutdev_win.geometry("400x650+600+100")
#         header_frame = ttk.Frame(aboutdev_win)
#         header_frame.pack(pady=20)

#         heading_label = ttk.Label(header_frame, text='About Developers', font=("Helvetica", 18, "bold"))
#         heading_label.pack(pady=10)

#         heading_line = ttk.Separator(aboutdev_win, orient="horizontal")
#         heading_line.pack(fill='x')

#         devs_frame = ttk.Frame(aboutdev_win)
#         devs_frame.pack(padx=20, pady=10)

#         developers_info = [
#             {
#                 'image_path': 'GUI/Images/Ns.png',
#                 'name': 'Developer 1',
#                 'description': 'This is a short bio of Developer 1.',
#                 'github_link': 'https://github.com/developer1',
#                 'linkedin_url': 'https://www.linkedin.com/in/developer1/',
#                 'email': 'developer1@example.com'
#             },
#             {
#                 # 'image_path': 'C:/Users/Raghavi/Desktop/photo.jpg',
#                 'name': 'Developer 2',
#                 'description': 'This is a short bio of Developer 1.',
#                 'github_link': 'https://github.com/developer1',
#                 'linkedin_url': 'https://www.linkedin.com/in/developer1/',
#                 'email': 'developer1@example.com'
#             },
#             {
#                 # 'image_path': 'C:/Users/Raghavi/Desktop/photo.jpg',
#                 'name': 'Developer 3',
#                 'description': 'This is a short bio of Developer 1.',
#                 'github_link': 'https://github.com/developer1',
#                 'linkedin_url': 'https://www.linkedin.com/in/developer1/',
#                 'email': 'developer1@example.com'
#             },
#             {
#                 # 'image_path': 'C:/Users/Raghavi/Desktop/photo.jpg',
#                 'name': 'Developer 4',
#                 'description': 'This is a short bio of Developer 1.',
#                 'github_link': 'https://github.com/developer1',
#                 'linkedin_url': 'https://www.linkedin.com/in/developer1/',
#                 'email': 'developer1@example.com'
#             }
#         ]

#         def create_developer_block(dev_info):
#             dev_frame = ttk.Frame(devs_frame)
#             dev_frame.pack(fill='x', pady=10)

#             try:
#                 image = Image.open(dev_info['image_path'])
#                 image = image.resize((100, 100), Image.ANTIALIAS)
#                 photo = ImageTk.PhotoImage(image)
#             except Exception as e:
#                 print(e)
#                 photo = None

#             if photo:
#                 img_label = ttk.Label(dev_frame, image=photo)
#                 img_label.image = photo
#                 img_label.pack(side='left', padx=10)
#             else:
#                 img_label = ttk.Label(dev_frame, text='Image not available')
#                 img_label.pack(side='left', padx=10)

#             details_frame = ttk.Frame(dev_frame)
#             details_frame.pack(side='left', padx=20)

#             ttk.Label(details_frame, text=dev_info['name'], font=('Arial', 12, 'bold')).pack(anchor='nw')

#             ttk.Label(details_frame, text=dev_info['description']).pack(anchor='nw')

#             github_link = ttk.Label(details_frame, text='GitHub', foreground="blue", cursor="hand2")
#             github_link.pack(anchor='nw')
#             github_link.bind("<Button-1>", lambda e: open_url(dev_info['github_link']))

#             linkedin_link = ttk.Label(details_frame, text='LinkedIn', foreground="blue", cursor="hand2")
#             linkedin_link.pack(anchor='nw')
#             linkedin_link.bind("<Button-1>", lambda e: open_url(dev_info['linkedin_url']))

#             email_link = ttk.Label(details_frame, text=dev_info['email'], foreground="blue", cursor="hand2")
#             email_link.pack(anchor='nw')
#             email_link.bind("<Button-1>", lambda e: open_url(f"mailto:{dev_info['email']}"))

#         for developer in developers_info:
#             create_developer_block(developer)

#         back_button = tk.Button(aboutdev_win, text='Back', bg='#FFA500', fg='white', font=('Helvetica', 10, 'bold'),
#                                 command=go_back)
#         back_button.pack(side='bottom', pady=10)

#         aboutdev_win.mainloop()
#     except Exception as e:
#         messagebox.showerror("Error",e)


import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser
import os

def aboutDevelopers_page():
    try:
        def open_url(url):
            webbrowser.open_new_tab(url)

        def go_back():
            aboutdev_win.destroy()

        aboutdev_win = tk.Toplevel()  # Create a Toplevel window
        aboutdev_win.title('About The Developers')
        aboutdev_win.geometry("400x650+600+100")
        header_frame = ttk.Frame(aboutdev_win)
        header_frame.pack(pady=20)

        heading_label = ttk.Label(header_frame, text='About Developers', font=("Helvetica", 18, "bold"))
        heading_label.pack(pady=10)

        heading_line = ttk.Separator(aboutdev_win, orient="horizontal")
        heading_line.pack(fill='x')

        devs_frame = ttk.Frame(aboutdev_win)
        devs_frame.pack(padx=20, pady=10)

        developers_info = [
            {
                'image_path': 'GUI/Images/Vrutti.png',
                'name': 'Vrutti Shingarpure',
                'description': 'This is a short bio of Developer 1.',
                # 'github_link': 'https://github.com/VruttiShringarpure382',
                'linkedin_url': 'http://www.linkedin.com/in/vrutti-shringarpure',
                'email': 'vrutti.shringarpure.developer@gmail.com'
            },
            {
                'image_path': 'GUI/Images/Nikita.png',
                'name': 'Nikita Talele',
                'description': 'This is a short bio of Developer 2.',
                # 'github_link': 'hhttps://github.com/NikitaRTalele',
                'linkedin_url': 'https://www.linkedin.com/in/nikita-talele-104514239/',
                'email': 'nikitatalele265@gmail.com'
            },
            {
                'image_path': 'GUI/Images/Ns.png',
                'name': 'Tanmay katke',
                'description': 'This is a short bio of Developer 3.',
                # 'github_link': 'https://github.com/developer3',
                'linkedin_url': 'https://www.linkedin.com/in/developer3/',
                'email': 'developer3@example.com'
            },
            {
                'image_path': 'GUI/Images/Raghavi.png',
                'name': 'Raghavi Shukla',
                'description': 'This is a short bio of Developer 4.',
                # 'github_link': 'https://github.com/developer4',
                'linkedin_url': 'https://www.linkedin.com/in/raghavi-a-shukla-1a658a244/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app',
                'email': 'raghavi.shukla224@gmail.com'
            }
        ]

        def create_developer_block(dev_info):
            dev_frame = ttk.Frame(devs_frame)
            dev_frame.pack(fill='x', pady=10)

            image_path = dev_info.get('image_path')
            if image_path and os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                except Exception as e:
                    print(e)
                    photo = None

                if photo:
                    img_label = ttk.Label(dev_frame, image=photo)
                    img_label.image = photo
                    img_label.pack(side='left', padx=10)
                else:
                    img_label = ttk.Label(dev_frame, text='Image not available')
                    img_label.pack(side='left', padx=10)
            else:
                img_label = ttk.Label(dev_frame, text='Image not found')
                img_label.pack(side='left', padx=10)

            details_frame = ttk.Frame(dev_frame)
            details_frame.pack(side='left', padx=20)

            ttk.Label(details_frame, text=dev_info['name'], font=('Arial', 12, 'bold')).pack(anchor='nw')

            ttk.Label(details_frame, text=dev_info['description']).pack(anchor='nw')

            # github_link = ttk.Label(details_frame, text='GitHub', foreground="blue", cursor="hand2")
            # github_link.pack(anchor='nw')
            # github_link.bind("<Button-1>", lambda e: open_url(dev_info['github_link']))

            linkedin_link = ttk.Label(details_frame, text='LinkedIn', foreground="blue", cursor="hand2")
            linkedin_link.pack(anchor='nw')
            linkedin_link.bind("<Button-1>", lambda e: open_url(dev_info['linkedin_url']))

            email_link = ttk.Label(details_frame, text=dev_info['email'], foreground="blue", cursor="hand2")
            email_link.pack(anchor='nw')
            email_link.bind("<Button-1>", lambda e: open_url(f"mailto:{dev_info['email']}"))

        for developer in developers_info:
            create_developer_block(developer)

        back_button = tk.Button(aboutdev_win, text='Back', bg='#FFA500', fg='white', font=('Helvetica', 10, 'bold'),
                                command=go_back)
        back_button.pack(side='bottom', pady=10)

        aboutdev_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)
