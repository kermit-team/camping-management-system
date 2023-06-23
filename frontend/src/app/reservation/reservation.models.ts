import { UserResponse } from "../shared/user.models";

export type SectionResponse = {
    id: number;
    name:string;
    plot_price: string;
    price_per_adult: string;
    price_per_child: string;
}
export type PlotResponse = {
    id: number;
    camping_section: SectionResponse;
    position: number;
}
export type ReservationResponse = {
    id: number;
    user: UserResponse;
    car: Car;
    camping_plot: PlotResponse;
    payment: Payment;
    date_from: string;
    date_to: string;
    number_of_adults: number;
    number_of_children: number;
    number_of_babies: number;
}
export type Car = {
    id: number;
    drivers: UserResponse[];
    registration_plate: string;
}
export type Payment = {
    id: number;
    status: string;
    stripe_checkout_id: string;
    price: number;
}
export type ReservationCreateResponse = {
    checkout_url: string;
    reservation: ReservationResponse
}
