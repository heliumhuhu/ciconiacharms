// Replace placeholders here. Prices for real products are integer pence.
// Null prices keep the owner's requested linked labels until actual prices are supplied.
export const shop = {address:'[shop address]',hours:'[opening hours]',contact:'[contact details]'};
export const products = Array.from({length:24},(_,i)=>({id:`product-${i+1}`,number:i+1,name:`[product${i+1}]`,category:i<12?'jewellery':'toys',description:`[description${i+1}]`,pricePence:null,priceLabel:`[price${i+1}]`,image:null,imageLabel:`[image${i+1}]`,alt:`[image${i+1}]`,displayOrder:i,visible:true}));
export function priceOf(p){return Number.isInteger(p.pricePence)?new Intl.NumberFormat('en-GB',{style:'currency',currency:'GBP'}).format(p.pricePence/100):p.priceLabel||'[price]';}
