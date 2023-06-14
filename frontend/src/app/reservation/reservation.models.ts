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
