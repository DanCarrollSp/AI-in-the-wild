#define PROTECT_H

#include "Droid.h"
#include "MoveTo.h"
#include <iostream>


class Protect : public Routine 
{
public:
    int protecteeId;//ID of the droid to protect
    int threatId;   //ID of the droid that poses a threat
    MoveTo* moveTo; //Pointer to a MoveTo routine handles movement

    //Initialise the protect behavior
    Protect(int protecteeId, int threatId, Grid& grid) : Routine(), protecteeId(protecteeId), threatId(threatId) 
    {
        this->routineType = "Protect";
        this->routineGrid = &grid;
        moveTo = nullptr;//Starts with no movement behavior set
    }

    //Starts protect routine, sets the state to Running
    void start(string msg) override 
    {
        std::cout << "--- Starting routine " << routineType << msg << std::endl;
        state = RoutineState::Running;
    }

    //Resets the protect routine, deletes previous MoveTo
    void reset(string msg) override 
    {
        std::cout << "--- Resetting routine " << routineType << msg << std::endl;
        if (moveTo) 
        {
            delete moveTo;//Free memory allocated to movement
            moveTo = nullptr;
        }
        state = RoutineState::None;//Resets state to None
    }

    //Executes the protect behavior, calculates the intercept position
    void act(Droid* droid, Grid& grid) override 
    {
        Droid* protectee = nullptr;//Pointer to the droid that needs protection
        Droid* threat = nullptr;   //Pointer to the threatener droid



        //Iterates through all droids in the grid to find the protectee and the threat
        //Using D1 and D3 (Yellow and Magenta) from the doc example
        for (Droid* other : grid.m_gridDroids) 
        {
            if (other->name == "D1") protectee = other;
            if (other->name == "D3") threat = other;
        }
        //If either the protectee or threat is missing we can just fail the routine
        if (!protectee || !threat) 
        {
            std::cout << "Protect routine failed: Missing protectee or threat." << std::endl;
            fail();
            return;
        }



        ///Moves protectee to the midpoint between D1 and D3 (I think this looks better/smarter overall as the protectee attempts to stay ahead of the player this way)
        //
        ////Calculates the midpoint
        //sf::Vector2f midPoint = (protectee->position + threat->position) / 2.0f;
        ////Converts the midpoint to the nearest grid cell coordinates
        //int targetX = grid.getGridCellX(sf::Vector2i(midPoint));
        //int targetY = grid.getGridCellY(sf::Vector2i(midPoint));



        ///This behaviour doesnt seems as smart looking as the one implemented above 
        ///but its the way it was done in the excel so i'll leave this one as default - feel free to comment it out and uncomment the above to take a look
        ///Thanks -Dan
        // 
        //Calcs closest protect point
        sf::Vector2f droidPos = droid->position;
        sf::Vector2f pPos = protectee->position;
        sf::Vector2f tPos = threat->position;

        //Generates multiple positions along the line between D1 and D3
        std::vector<sf::Vector2f> possiblePositions;
        int numSteps = 8;//Amount of points were generating (10 is fine for this gridsize)
        for (int i = 1; i < numSteps; ++i)
        {
            float t = static_cast<float>(i) / numSteps;
            sf::Vector2f interpolatedPos = (1 - t) * pPos + t * tPos;
            possiblePositions.push_back(interpolatedPos);
        }

        //Finds the nearest valid position to the droid out of the generated
        sf::Vector2f bestPos = possiblePositions[0];
        float minDist = std::numeric_limits<float>::max();

        for (const sf::Vector2f& pos : possiblePositions)
        {
            float dist = std::hypot(droidPos.x - pos.x, droidPos.y - pos.y);
            if (dist < minDist)
            {
                minDist = dist;
                bestPos = pos;
            }
        }

        //Converts to grid coords
        int targetX = grid.getGridCellX(sf::Vector2i(bestPos));
        int targetY = grid.getGridCellY(sf::Vector2i(bestPos));



        //If moveTo is not already set, create a new movement behavior
        if (!moveTo) 
        {
            moveTo = new MoveTo(targetX, targetY, grid);
            moveTo->start(" from Protect node.");
        }

        //Perform the movements of the droids pos
        moveTo->act(droid, grid);



        //If movement is successful, mark the protect routine as successful
        //Else if movement fails, mark the Protect routine as failed
        if (moveTo->isSuccess()) succeed("Protect routine completed for " + droid->name);
        else if (moveTo->isFailure()) fail();
    }
};