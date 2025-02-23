<!-- PROJECT LOGO -->
<div align="center">

<h3 align="center">Tranga-Manager</h3>

  <p align="center">
    Manager for multiple instances of Tranga-API
  </p>
  <p align="center">
    This is the manager for <a href="https://github.com/C9Glax/tranga">Tranga</a> (API)  
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Tranga-Manager is the manager/proxy to [Tranga](https://github.com/C9Glax/tranga) (the API). It displays information aquired from Tranga and can create Jobs (Manga-Downloads).

### What this does do (and nothing else)

This project proxies request to [Tranga-API](https://github.com/C9Glax/tranga) through server side code alowing it to display it's present configurations even without direct access to the API.

### Built With

- Django, Python
- HTML, CSS, and barebones Javascripts

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

There is a single release:

### Docker

Download [docker-compose.yaml](https://github.com/Makhuta/tranga-manager/blob/main/docker-compose.yaml) and configure to your needs. 
The `docker-compose` also includes [Tranga](https://github.com/C9Glax/tranga) as backend. For its configuration refer to the repo README.

#### Environmental Variables

| Name | Default | Required | Description |
| - | - | - | - |
| ```DEBUG``` | False | False | Enables debug for Django |
| ```SECRET_KEY``` |  | True | Secret key for Django |
| ```ALLOWED_HOSTS``` | * | False | List of allowed hosts separated with "," |
| ```DJANGO_USERNAME``` | Admin | False (Recommended) | Manager Login username |
| ```DJANGO_PASSWORD``` | tranga-admin | False (Recommended) | Manager Login password |
| ```DJANGO_EMAIL``` | default@email.com | False | Manager Login email (not currently used for anything) |
| ```DATABASE_DIR``` | /app | False (Recommended) | Directory in which the db.sqlite3 will be saved (highly recomended to use for keeping the connections/added APIs) |
| ```CSRF_TRUSTED_ORIGINS``` | localhost:80,127.0.0.1:80 | False | Truested origins that will be used for CSRF |

<!-- ROADMAP -->
## Roadmap

- [ ] ❓

See the [open issues](https://github.com/Makhuta/tranga-manager/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

The following is copy & pasted:

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Font Awesome](https://fontawesome.com)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/tree/master)

<p align="right">(<a href="#readme-top">back to top</a>)</p>