import axios from 'axios';
axios.defaults.withCredentials = true;
import { base_url } from '../config';

// ..................................... user and admin login and register api calls..................................................

export function getuser(jwt){
    return axios({
        method: 'get',
        url: base_url + 'getuser',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function getadmin(jwt){
    return axios({
        method: 'get',
        url: base_url + 'getadmin',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function updateuser(userdata, jwt){
    return axios({
        method: 'put',
        url: base_url + 'userupdate',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            email: userdata['email'],
            password: userdata['password'],
            name: userdata['name']
        }
    })
}

export function updateadmin(userdata, jwt){
    return axios({
        method: 'put',
        url: base_url + 'adminupdate',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            email: userdata['email'],
            password: userdata['password'],
            name: userdata['name']
        }
    })
}

export function deleteuser(jwt){
    return axios({
        method: 'delete',
        url: base_url + 'userdelete',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function deleteadmin(jwt){
    return axios({
        method: 'delete',
        url: base_url + 'admindelete',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function authenticate(userdata, jwt) {
    return axios({
        method: 'post',
        url: base_url + 'userlogin',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data: {
            email: userdata['username'],
            password: userdata['password']
        }
    })
}

export function register(userdata) {
    return axios({
        method: 'post',
        url: base_url + 'userregister',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data: {
            email: userdata['username'],
            password: userdata['password'],
            name: userdata['name']
        }
    })
}

export function adminregister(userdata) {
    return axios({
        method: 'post',
        url: base_url + 'adminregister',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data: {
            email: userdata['username'],
            password: userdata['password'],
            name: userdata['name']
        }
    })
}


export function adminauthenticate(userdata) {
    return axios({
        method: 'post',
        url: base_url + 'adminlogin',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data: {
            email: userdata['username'],
            password: userdata['password']
        }
    })
}

export function generatecsv(jwt){
    return axios({
        method: 'get',
        url: base_url + 'generatecsv',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })

}

// ............................................................venue api calls..................................................

export function getvenues(jwt) {
    return axios({
        method: 'get',
        url: base_url + 'getvenue',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function getvenuesbyadmin(jwt) {
    return axios({
        method: 'get',
        url: base_url + 'getvenuebyadmin',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function addvenue(venue, jwt) {
    console.log(venue)
    return axios({
        method: 'post',
        url: base_url + 'addvenue',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            name: venue['name'],
            location: venue['location'],
            capacity: venue['capacity'],
            price: venue['price'],
            description: venue['description'],
            image: venue['image']
        }
    })
}

export function editvenue(venue, jwt) {
    console.log(venue)
    return axios({
        method: 'put',
        url: base_url + 'editvenue',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            venue_id: venue['id'],
            name: venue['name'],
            location: venue['location'],
            capacity: venue['capacity'],
            description: venue['description'],
            image: venue['image'],
        }
    })
}


export function delvenue(venueid, jwt) {
    console.log(venueid)
    return axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/deletevenue',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            venue_id: venueid
        }
    })
}

// ............................................................movie/shows api calls..................................................

export function getshows(venueid, jwt) {
    console.log(venueid)
    return axios({
        method: 'get',
        url: base_url + 'getshow/' + venueid[0] + '/' + venueid[1],
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function freeslots(showd, jwt) {
    console.log(showd)
    return axios({
        method: 'post',
        url: base_url + 'getfreeslots',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            date: showd['date'],
            venue_id: showd['venue_id'],
            duration: showd['duration'],
        }
    })
}

export function addshow(show, jwt) {
    console.log(show)
    return axios({
        method: 'post',
        url: base_url + 'addshow',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            date: show['date'],
            venue_id: show['venue_id'],
            duration: show['duration'],
            movie: show['movie'],
            price: show['price'],
            image: show['image'],
            description: show['description'],
            tags: show['tags'],
        }
    })
}

export function editshow(show, jwt) {
    console.log(show)
    return axios({
        method: 'put',
        url: base_url + 'editshow',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            venue_id: show['venue_id'],
            show_id: show['id'],
            date: show['date'],
            venue_id: show['venue_id'],
            duration: show['duration'],
            movie: show['movie'],
            price: show['price'],
            image: show['image'],
            description: show['description'],
            tags: show['tags'],
        }
    })
}

export function ableshow(showid, jt) {
    return axios({
        method: 'put',
        url: base_url + 'ableshow',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jt,
        },
        data: {
            show_id: showid,
        }
    })

}

export function delshow(showid, jt) {
    return axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/deleteshow',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jt,
        },
        data: {
            show_id: showid,
        }
    })

}

// ............................................................booking api calls..................................................

export function book(show, jwt) {
    console.log(show)
    return axios({
        method: 'post',
        url: base_url + 'bookshow',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            show_id: show['show_id'],
            quantity: show['quantity'],
            total: show['total'],
            date: show['date'],
            movie: show['movie'],
            venue: show['venue'],
        }
    })
}

export function getbookings(jwt) {
    return axios({
        method: 'get',
        url: base_url + 'getuserbooking',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
    })
}

export function rateshow(show, jwt) {
    console.log(show)
    return axios({
        method: 'put',
        url: base_url + 'rateshow',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            show_id: show['show_id'],
            rating: show['rating'],
            book_id : show['id']
        }
    })
}

export function getchart(showid, jwt) {
    return axios({
        method: 'post',
        url: base_url + 'getchart',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + jwt,
        },
        data: {
            show_id: showid,
        }
    })
}