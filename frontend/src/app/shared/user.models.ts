export type UserResponse = {
    email: string;
    first_name: string;
    last_name: string;
    phone_number: number;
    avatar: string;
    id_card: string;
    cars: number[];
    groups: Groups[];
}

export type Groups = {
     id: number;
     name: string;
}

export type FullUserResponse = {
    email: string;
    first_name: string;
    last_name: string;
    phone_number: number;
    avatar: string;
    id_card: string;
    cars: number[];
    groups: Groups[];
    id: number;
}

export type FullUserRequest = {
    email: string;
    first_name: string;
    last_name: string;
    phone_number: number;
    avatar: string;
    id_card: string;
    cars: number[];
    groups: number[];
    id: number;
}