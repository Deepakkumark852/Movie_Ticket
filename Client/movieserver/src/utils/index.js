import mitt from 'mitt'

export const EventBus = new mitt()

export function isValidJwt(jwt) {
    if (jwt == "" || jwt == null) {
        console.log('jwt2', jwt)
        return false
    }
    else {
        if (jwt['jwt'] != undefined){
            jwt = jwt['jwt']
        }
        if (!jwt || jwt.split('.').length < 3) {
            return false
        }
        const data = JSON.parse(atob(jwt.split('.')[1]))
        const exp = new Date(data.exp * 1000) // JS deals with dates in milliseconds since epoch
        const now = new Date()
        return now < exp
    }
}

export function uservalid(jwt) {
    if (jwt == "" || jwt == null) {
        console.log('jwt2', jwt)
        return false
    }
    else {
        if (jwt['jwt'] != undefined){
            jwt = jwt['jwt']
        }
        if (!jwt || jwt.split('.').length < 3) {
            return false
        }
        const data = JSON.parse(atob(jwt.split('.')[1]))
        if ([0,2].includes(data['role'])){
            return true
        }
        else{
            return false
        }
    }
}

export function adminvalid(jwt) {
    if (jwt == "" || jwt == null) {
        console.log('jwt2', jwt)
        return false
    }
    else {
        if (jwt['jwt'] != undefined){
            jwt = jwt['jwt']
        }
        if (!jwt || jwt.split('.').length < 3) {
             
            return false
        }
        const data = JSON.parse(atob(jwt.split('.')[1]))
        
        if ([1,2].includes(data['role'])){
            return true
        }
        else{
            return false
        }
    }
}
