# Yulon Nissan Motor
#### Background: Analyzing the car data of driving and GPS from Yulon Nissan Motor, exploring insights, and then recommending a proposal with business value.

#### Target: Building features to distinguish different drivers, clustering them, and finally, suggesting fitted vehicles.

#### Models: K-Means, Affinity Propagation, Hierarchical Clustering 

## Introdution 
- Target Audience(TA): Car owners who existed from 2019 to 2022 (1298 in total) and ranged between January 2022 and June 2022. Additionally, the feature of receiving satellite data is set to true in order to explicitly capture driving information.
- Finding of EDA:
 1. Majority of car is K car.
 2. Speed density plot
<img width="532" alt="Screenshot 2023-11-26 at 20 21 57" src="https://github.com/WSY-Samuel/Yulon-Nissan-Motor/assets/87291914/b13fc627-fabe-4a4e-9342-9e7ffea25cfa">

3. Speed plot

3.1 speed with 0  
<img width="369" alt="Screenshot 2023-11-26 at 20 23 14" src="https://github.com/WSY-Samuel/Yulon-Nissan-Motor/assets/87291914/1a93717a-79f4-415a-9b4e-e5b9ad64c317">
 
 3.2 speed without 0  
<img width="391" alt="Screenshot 2023-11-26 at 20 24 20" src="https://github.com/WSY-Samuel/Yulon-Nissan-Motor/assets/87291914/175933ed-85ff-47f9-9ace-026b0b8d9f78">

4. Mile density plot
<img width="561" alt="Screenshot 2023-11-26 at 20 25 11" src="https://github.com/WSY-Samuel/Yulon-Nissan-Motor/assets/87291914/12092c55-cb66-4d90-9ff2-f5d4024feec1">

## Featuring Engineering:
1. Mileage(Weekdays vs. Weekends) : Short(0-20km), Medium(20-60km), Long(60km~) Term.
2. Speed: Over 100km or not.
3. School(elementary/junior): Checking if the driver stops within 300 meters between 07:00-18:00 to determine if there are kids in the family.
4. Obstetrics and Gynecology:Verifying driver stops within 500 meters to identify potential newborns in the family.
5. Hypermarket(costco, carrefour etc): Identifying driver stops within 200 meters to assess the need for a more spacious car.
6. Electric vehicle charging pile: Checking suitable for Nissan charging stations within 1km to recommend electric cars to them.
7. Driving counts: Computing the total driving counts for each car owners.
8. Camping area: Verifying driver stops within 200 meters to identify camping habits.

## Conclusion
Comparing three clustering algorithms, I believe that the group results of K-Means and Affinity Propagation have better interpretability. Therefore, I have decided to optimize them.

The optimization process includes:
1. Dropping the camping area feature.
2. Verifying the number of groups using the Silhouette Coefficient. The highest score obtained is 5.

<img width="414" alt="Screenshot 2023-11-27 at 20 13 40" src="https://github.com/WSY-Samuel/Yulon-Nissan-Motor/assets/87291914/1edcccc2-b228-4bdd-a999-b57800b46f43">  

Based on the above, I calculated the clustering results for recommending cars using the Calinski-Harabasz index and Davies-Boudin index. After optimization, the clustering results for features, driver ID, and data counts are very close between the two algorithms.
 
<img width="568" alt="Screenshot 2023-11-27 at 20 27 49" src="https://github.com/WSY-Samuel/Yulon-Nissan-Motor/assets/87291914/8ceb72bf-1350-4e5f-b8bf-7d98800fc7bf">  

According to the calculations, the results of K-Means have a higher score on the Calinski-Harabasz index and a lower score on the Davies-Boudin index. Finally, I chose the labels of clustering by K-Means for recommending cars.

